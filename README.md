# ⚖️ LegalEagle AI - Enterprise Contract Intelligence

## 📌 Overview

This project aims to build an **AI-powered legal auditor** to democratize legal access for freelancers and SMEs. It includes **forensic contract analysis, risk scoring, and smart drafting** using Google's Gemini 1.5 Pro model.
The system processes complex legal PDFs, identifying liabilities and non-compliance with the **Indian Contract Act, 1872**, enabling users to sign agreements with confidence.

## 🚀 Tech Stack Used

🐍 **Python** – for core logic and backend processing
📊 **Streamlit** – for the interactive web dashboard
🧠 **Google Gemini 1.5 Pro** – for legal reasoning and generative AI
🤖 **SpaCy** – for Natural Language Processing (NLP) and entity recognition
📄 **PDFPlumber** – for high-fidelity document text extraction
📉 **Plotly** – for risk visualization and gauge charts
🔐 **Python-Dotenv** – for secure API key management

## 📂 Data & Inputs

The system processes unstructured legal data including:
✔ **PDF/DOCX Contracts** (NDAs, Employment, Lease Deeds)
✔ **Legal Clauses** (Indemnity, Termination, Liability)
✔ **User Queries** (Natural language legal questions)
✔ **Drafting Parameters** (Party names, Jurisdiction, Terms)

## 🛠 Preprocessing Steps:

✅ **Text Extraction:** Parsing raw text from PDF/DOCX files
✅ **PII Redaction:** Automating the removal of emails and phone numbers (Privacy Shield)
✅ **Clause Segmentation:** Breaking down long contracts into analyzable chunks
✅ **Context Windowing:** Optimizing token usage for the Gemini API

## 🔥 AI Processing Pipeline

### 📌 Risk Engine:
✅ **Clause Cross-Referencing:** Checking against Indian Contract Act, 1872
✅ **Liability Detection:** Flagging "Unlimited Liability" and "Unfair Termination"
✅ **Scoring Algorithm:** Calculating a quantitative Risk Score (0-100)

### 🏆 Generative Capabilities:
✅ **Legal Q&A:** Context-aware chatbot for specific contract questions
✅ **Smart Drafting:** Generating legally binding agreements for specific Indian cities
✅ **Plain English Summaries:** Converting "Legalese" into simple terms

## 📊 Key Metrics & Evaluation:

✅ **Risk Score (0-100):** Quantitative assessment of contract safety
✅ **Compliance Flags:** Red/Orange/Green alerts for clauses
✅ **Jurisdiction Check:** Verifying validity within Indian Law
✅ **Response Latency:** Real-time analysis (<10 seconds)

## 📈 Visualization Techniques:

✅ **Risk Gauge Meter** (Green = Safe, Red = Critical)
✅ **Expandable Risk Cards** for detailed clause analysis
✅ **Chat Interface** for interactive legal queries
✅ **Professional PDF Reports** for export

## 🌍 Model Deployment using Streamlit

1️⃣ User uploads a PDF contract via the web dashboard
2️⃣ **Gemini 1.5 Pro** analyzes the document in real-time
3️⃣ Risk Score and specific warnings are displayed on the dashboard
4️⃣ User can draft new contracts or ask follow-up questions

## 🛠 Installation and Setup

# 1️⃣ Clone the Repository
git clone https://github.com/SachinAnthony1422/legal-risk-auditor.git
cd legal-risk-auditor

# 2️⃣ Install Dependencies
pip install -r requirements.txt

# 3️⃣ Configure API Key
# Create a .env file in the root directory and add:
# GEMINI_API_KEY="your_api_key_here"

# 4️⃣ Run Streamlit App
streamlit run main.py

🔗 Open http://localhost:8501 in your browser to access the web application.

## 💡 Usage

1️⃣ **Upload:** Drag & drop any legal contract (PDF) on the "Audit Dashboard".
2️⃣ **Analyze:** Click "Run Forensic Audit" to generate the Risk Score.
3️⃣ **Chat:** Switch to "Legal Chat" to ask questions like *"Is the notice period fair?"*.
4️⃣ **Draft:** Use the "Drafter" tab to generate new agreements instantly.

## 🔮 Future Enhancements

☁ **Cloud Storage:** Integration with AWS S3/Google Drive for document history
🧠 **Multi-Modal Analysis:** OCR support for handwritten signatures/notes
📊 **Contract Comparison:** Diff-checker for Version A vs. Version B
🎨 **Regional Language Support:** Hindi/Tamil legal translation

🚀 **Happy Coding!**