# ⚖️ LegalEagle AI - Enterprise Contract Intelligence

## 📌 Overview

**LegalEagle AI** is an advanced legal auditing tool designed to democratize legal access for freelancers, SMEs, and individuals.

It uses **Google Gemini 1.5 Pro** to perform forensic analysis on contracts, automatically detecting liabilities, unfair terms, and non-compliance with the **Indian Contract Act, 1872**.

---

## 🚀 Tech Stack Used

* **🐍 Python** – Core logic and backend processing
    
* **📊 Streamlit** – Interactive web dashboard
    
* **🧠 Google Gemini 1.5 Pro** – Legal reasoning and generative AI
    
* **🤖 SpaCy** – Natural Language Processing (NLP) & entity recognition
    
* **📄 PDFPlumber** – High-fidelity document text extraction
    
* **📉 Plotly** – Risk visualization and gauge charts
    
* **🔐 Python-Dotenv** – Secure API key management

---

## 📂 Data & Inputs

The system is built to process unstructured legal data, including:

* ✔ **PDF/DOCX Contracts** (NDAs, Employment Agreements, Lease Deeds)
    
* ✔ **Legal Clauses** (Indemnity, Termination, Liability, Non-Compete)
    
* ✔ **User Queries** (Natural language legal questions like *"Is this fair?"*)
    
* ✔ **Drafting Parameters** (Party names, Jurisdiction, Specific Terms)

---

## 🛠 Preprocessing Steps

* ✅ **Text Extraction:** Parsing raw text from PDF/DOCX files with layout preservation.
    
* ✅ **PII Redaction:** Automating the removal of emails and phone numbers (Privacy Shield).
    
* ✅ **Clause Segmentation:** Breaking down long contracts into analyzable chunks.
    
* ✅ **Context Windowing:** Optimizing token usage for the Gemini API.

---

## 🔥 AI Processing Pipeline

### 📌 Risk Engine
* ✅ **Clause Cross-Referencing:** Checks against Indian Contract Act, 1872.
* ✅ **Liability Detection:** Flags "Unlimited Liability" and "Unfair Termination".
* ✅ **Scoring Algorithm:** Calculates a quantitative Risk Score (0-100).

### 🏆 Generative Capabilities
* ✅ **Legal Q&A:** Context-aware chatbot for specific contract questions.
* ✅ **Smart Drafting:** Generates legally binding agreements for specific Indian cities.
* ✅ **Plain English Summaries:** Converts complex "Legalese" into simple terms.

---

## 📊 Key Metrics & Evaluation

* **Risk Score (0-100):** Quantitative assessment of contract safety.
    
* **Compliance Flags:** Red/Orange/Green alerts for specific clauses.
    
* **Jurisdiction Check:** Verifying validity within Indian Law.
    
* **Response Latency:** Real-time analysis (<10 seconds).

---

## 🌍 Model Deployment (Streamlit)

1.  User uploads a **PDF contract** via the web dashboard.
    
2.  **Gemini 1.5 Pro** analyzes the document text in real-time.
    
3.  **Risk Score** and specific warnings are displayed on the dashboard.
    
4.  User can **Chat** with the document or **Draft** new terms.

---

## 🛠 Installation and Setup

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/SachinAnthony1422/legal-risk-auditor.git](https://github.com/SachinAnthony1422/legal-risk-auditor.git)
cd legal-risk-auditor

### 3️⃣ Configure API Key
Create a .env file in the root directory and add your key:
```bash
GEMINI_API_KEY="your_api_key_here"

### 4️⃣ Run Streamlit App
```bash
streamlit run main.py

---

🔗 Access the App: Open http://localhost:8501 in your browser.

---

##💡 **Usage Guide**

1. **Upload:** Drag & drop any legal contract (PDF) on the "Audit Dashboard".

2. **Analyze:** Click "Run Forensic Audit" to generate the Risk Score.

3. **Chat:** Switch to "Legal Chat" to ask questions like "Is the notice period fair?".

4. **Draft:** Use the "Drafter" tab to generate new agreements instantly.

---

##🔮 **Future Enhancements**

1. **☁ Cloud Storage:** Integration with AWS S3/Google Drive for document history.

2. **🧠 Multi-Modal Analysis:** OCR support for handwritten signatures/notes.

3. **📊 Contract Comparison:** Diff-checker for Version A vs. Version B.

4. **🎨 Regional Language Support:** Hindi/Tamil legal translation.