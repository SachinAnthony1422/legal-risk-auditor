import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key safely
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class LegalRiskEngine:
    def __init__(self):
        # Using your working model
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def analyze_contract(self, contract_text: str):
        """
        Hybrid Analysis:
        1. Tries Real AI (Gemini) with Multilingual Prompt.
        2. If Quota Exceeded (429) or Error -> Falls back to Mock Data.
        """
        
        # --- THE POLYGLOT PROMPT UPGRADE ---
        prompt = f"""
        You are a Senior Corporate Lawyer in India. 
        INPUT CONTEXT: The user has uploaded a contract. It might be in English or Hindi (Devanagari script).
        
        TASK:
        1. If the contract is in Hindi, translate the legal concepts internally to analyze them against the Indian Contract Act 1872.
        2. Identify the TOP 3-4 most risky clauses for a small business owner (SME).
        3. Assign a 'Risk Score' (0-100).
        4. Provide summaries and explanations in TWO languages: English and Hindi.

        OUTPUT FORMAT:
        You must return strictly Valid JSON. Do not add markdown.
        {{
            "overall_score": 85,
            "risk_level": "High/Medium/Low",
            "detected_language": "English OR Hindi",
            "summary_english": "Plain English summary...",
            "summary_hindi": "Hindi summary translation...",
            "clauses": [
                {{
                    "original_text": "Paste the exact text from the document (keep Hindi if original is Hindi)",
                    "risk_score": 90,
                    "explanation_english": "Why this is dangerous...",
                    "explanation_hindi": "Hindi explanation...",
                    "recommendation": "Negotiation advice..."
                }}
            ]
        }}

        CONTRACT TEXT:
        {contract_text[:20000]}
        """

        try:
            # 1. Try Real AI
            response = self.model.generate_content(prompt)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)

        except Exception as e:
            # 2. Fallback to Mock Data (Safety Net)
            print(f"⚠️ Limit Hit or Error ({e}). Switching to Demo Mode.")
            return self._mock_data()

    def _mock_data(self):
        """
        Safe Demo Data with Hindi translations pre-filled.
        """
        time.sleep(2)
        return {
            "overall_score": 88,
            "risk_level": "High",
            "summary_english": "DEMO MODE: This Agreement contains critical risks regarding liability caps and unilateral termination. It appears heavily weighted in favor of the Client.",
            "summary_hindi": "डेमो मोड: इस अनुबंध में दायित्व सीमा और एकतरफा समाप्ति के संबंध में गंभीर जोखिम हैं। यह ग्राहक के पक्ष में भारी प्रतीत होता है।",
            "clauses": [
                {
                    "original_text": "The Service Provider shall indemnify the Client for any and all losses...",
                    "risk_score": 95,
                    "explanation_english": "CRITICAL RISK (Section 124): 'Unlimited Indemnity'. This exposes your SME to infinite liability.",
                    "explanation_hindi": "गंभीर जोखिम (धारा 124): 'असीमित क्षतिपूर्ति'। यह आपके व्यवसाय को अनंत दायित्व के लिए उजागर करता है।",
                    "recommendation": "Negotiate a 'Liability Cap' limited to 100% of the total contract value."
                },
                {
                    "original_text": "The Client may terminate this Agreement at any time, for any reason, without prior notice.",
                    "risk_score": 90,
                    "explanation_english": "HIGH RISK: 'Unilateral Termination'. This violates principles of fair trade.",
                    "explanation_hindi": "उच्च जोखिम: 'एकतरफा समाप्ति'। यह निष्पक्ष व्यापार के सिद्धांतों का उल्लंघन करता है।",
                    "recommendation": "Require a mutual 'Notice Period' of at least 30 days for termination."
                }
            ]
        }