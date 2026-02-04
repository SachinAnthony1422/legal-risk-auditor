# ⚖️ Legal Risk Auditor (Powered by Gemini AI)

**A Next-Gen AI Tool for Automating Legal Contract Review and Risk Assessment.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://legal-risk-auditor.streamlit.app/)

## 🚀 Live Demo
**[Click Here to Try the App](https://legal-risk-auditor.streamlit.app/)**

---

## 📖 Project Overview
Submitted for the **HCL GUVI Hackathon**.
Legal Risk Auditor automates contract review using **Google Gemini 1.5 Pro**. It allows users to upload PDF contracts, instantly detecting high-risk clauses, summarizing key terms, and suggesting safer legal language.

### 🌟 Key Features
* **📄 PDF Contract Analysis:** Extracts text from scanned or digital PDFs.
* **⚠️ Automatic Risk Detection:** Identifies dangerous clauses (Indemnity, Termination).
* **🤖 AI-Powered Q&A:** Ask questions like *"Is the termination clause fair?"*
* **📝 Automated Drafting:** Generates new legal clauses based on user inputs.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Model:** Google Gemini 1.5 Pro
* **NLP Engine:** SpaCy & PDFPlumber
* **Language:** Python 3.11

---

## ⚙️ How to Run Locally
1.  **Clone the Repository**
2.  **Install Dependencies:** `pip install -r requirements.txt`
3.  **Add API Key:** Create `.env` file with `GEMINI_API_KEY`
4.  **Run:** `streamlit run main.py`