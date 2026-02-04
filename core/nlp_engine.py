import spacy
import re
from typing import List, Dict, Any

class LegalNLPEngine:
    """
    The Pre-Processing 'Eyes'.
    Uses spaCy for fast entity extraction and Regex for clause segmentation.
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Auto-download if missing
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def detect_language(self, text: str) -> str:
        # Checks for Hindi Unicode characters
        hindi_chars = re.findall(r'[\u0900-\u097F]', text)
        return "Hindi" if len(hindi_chars) > 50 else "English"

    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        Extracts: Parties (ORG), Money (MONEY), Dates (DATE).
        """
        doc = self.nlp(text)
        metadata = {
            "parties": [],
            "dates": [],
            "money": [],
            "obligations": [] # To be filled by keywords
        }

        for ent in doc.ents:
            if ent.label_ == "ORG":
                metadata["parties"].append(ent.text)
            elif ent.label_ == "DATE":
                metadata["dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                metadata["money"].append(ent.text)
        
        # Simple rule-based obligation detector (Advanced Feature)
        keywords = ["shall", "must", "agree", "undertake", "liable"]
        for sent in doc.sents:
            if any(k in sent.text.lower() for k in keywords):
                if len(sent.text) < 200: 
                    metadata["obligations"].append(sent.text)

        # Remove duplicates
        metadata["parties"] = list(set(metadata["parties"]))
        metadata["money"] = list(set(metadata["money"]))
        
        return metadata

    def segment_clauses(self, text: str) -> List[str]:
        """
        Crucial: Splits legal blob into analyze-able chunks.
        Looks for patterns like '1.', '2.1', 'ARTICLE I'.
        """
        pattern = r'(?:\n\s*|^)(?:\d+\.?\d*|SECTION\s+\d+|ARTICLE\s+[IVX]+)\s+'
        segments = re.split(pattern, text, flags=re.IGNORECASE)
        return [s.strip() for s in segments if len(s.strip()) > 50]