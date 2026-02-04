import streamlit as st
# --- MAGIC FIX FOR SPACY MODEL ---
import os
import spacy.cli
try:
    spacy.load("en_core_web_sm")
except OSError:
    print("Downloading language model...")
    spacy.cli.download("en_core_web_sm")
import time
import google.generativeai as genai
import os
import plotly.graph_objects as go
import re
from dotenv import load_dotenv

# Import Custom Modules
from core.document_parser import DocumentParser
from core.nlp_engine import LegalNLPEngine
from core.risk_engine import LegalRiskEngine
from utils.helpers import generate_pdf_report

# Load Environment
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="LegalEagle AI | Enterprise Edition",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Public Ready" Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Metrics Cards */
    .metric-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #2C5364;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px;
        color: #333;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2C5364;
        color: white;
    }
    
    /* Chat Message Styling */
    .chat-user {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .chat-ai {
        background-color: #f1f8e9;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---

def create_gauge_chart(score):
    """Draws a professional Risk Gauge."""
    color = "green"
    if score > 40: color = "orange"
    if score > 75: color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Compliance Risk Score", 'font': {'size': 18, 'color': "#333"}},
        number = {'font': {'size': 40, 'color': color}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 40], 'color': '#e8f5e9'},
                {'range': [40, 75], 'color': '#fff3e0'},
                {'range': [75, 100], 'color': '#ffebee'}],
        }
    ))
    fig.update_layout(height=230, margin={'t': 30, 'b': 0, 'l': 20, 'r': 20}, font={'family': "Inter"})
    return fig

def anonymize_text(text):
    """Simple PII redaction (Privacy Shield)"""
    # Redact Emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[REDACTED_EMAIL]", text)
    # Redact Phone Numbers (Simple Pattern)
    text = re.sub(r'\b\d{10}\b', "[REDACTED_PHONE]", text)
    return text

# --- 3. MAIN APPLICATION ---
def main():
    
    # Header
    st.markdown('<div class="main-header"><h1>⚖️ LegalEagle AI</h1><p>Enterprise-Grade Contract Intelligence for Indian SMEs</p></div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2666/2666505.png", width=60)
        st.markdown("### Control Center")
        
        st.markdown("---")
        st.markdown("**🛡️ Privacy Shield**")
        privacy_mode = st.toggle("Anonymize Personal Data", value=False, help="Masks emails and phones before sending to AI.")
        
        st.markdown("---")
        st.info("✅ **System Status:** Online\n\n✅ **Encryption:** AES-256\n\n✅ **Model:** Gemini 2.5 Flash")

    # TABS
    tab1, tab2, tab3 = st.tabs(["📊 Audit Dashboard", "🤖 Legal Chat Assistant", "📝 Contract Drafter"])

    # ----------------------------------------------------
    # TAB 1: AUDIT DASHBOARD (Main Analysis)
    # ----------------------------------------------------
    with tab1:
        col_up1, col_up2 = st.columns([2, 1])
        with col_up1:
            uploaded_file = st.file_uploader("Upload Agreement (PDF/DOCX)", type=['pdf', 'docx'])
        with col_up2:
            st.markdown("### ") # Spacing
            if uploaded_file and st.button("🚀 Analyze Now", type="primary"):
                st.session_state['analyzing'] = True

        if uploaded_file:
            # 1. Parse
            if 'doc_text' not in st.session_state:
                with st.spinner("Extracting text from document..."):
                    raw_text, error = DocumentParser.parse_file(uploaded_file)
                    if error:
                        st.error(error)
                        st.stop()
                    st.session_state['doc_text'] = raw_text
                    st.toast("Document uploaded successfully!", icon="✅")

            text_to_analyze = st.session_state['doc_text']
            
            # Privacy Layer
            if privacy_mode:
                text_to_analyze = anonymize_text(text_to_analyze)
                st.toast("Privacy Shield Active: Personal Data Redacted.", icon="🛡️")

            # 2. Analyze (Triggered by button)
            if st.session_state.get('analyzing', False):
                risk_engine = LegalRiskEngine()
                with st.status("🔍 Conducting Forensic Legal Audit...", expanded=True):
                    st.write("Reading clauses...")
                    time.sleep(0.5)
                    st.write("Cross-referencing Indian Contract Act 1872...")
                    time.sleep(0.5)
                    st.write("Generating Risk Score...")
                    
                    result = risk_engine.analyze_contract(text_to_analyze)
                    st.session_state['analysis_result'] = result
                    st.session_state['analyzing'] = False # Reset trigger
                    st.rerun()

            # 3. Display Dashboard
            if 'analysis_result' in st.session_state:
                res = st.session_state['analysis_result']
                
                # Language Toggle
                lang = st.radio("Display Language:", ["English", "Hindi"], horizontal=True, label_visibility="collapsed")
                is_hindi = lang == "Hindi"

                # Top Metrics
                m1, m2, m3 = st.columns(3)
                m1.markdown(f"<div class='metric-container'><div>Overall Risk</div><div class='metric-value'>{res.get('overall_score')}/100</div></div>", unsafe_allow_html=True)
                m2.markdown(f"<div class='metric-container'><div>Clauses Flagged</div><div class='metric-value'>{len(res.get('clauses', []))}</div></div>", unsafe_allow_html=True)
                m3.markdown(f"<div class='metric-container'><div>Jurisdiction</div><div class='metric-value'>India</div></div>", unsafe_allow_html=True)

                st.markdown("---")

                # Main Layout
                c_left, c_right = st.columns([1, 2])
                
                with c_left:
                    # Gauge
                    st.plotly_chart(create_gauge_chart(res.get('overall_score')), use_container_width=True)
                    
                    # Export
                    st.markdown("### 📤 Export")
                    official = st.checkbox("Official Report (No Watermark)")
                    report_data = generate_pdf_report(res, is_draft=not official)
                    st.download_button("Download PDF Report", data=report_data, file_name="Legal_Audit_Report.pdf", mime="application/pdf", use_container_width=True)

                with c_right:
                    # Summary & Risks
                    st.subheader("📋 Executive Summary")
                    summary = res.get('summary_hindi') if is_hindi else res.get('summary_english')
                    st.info(summary)
                    
                    st.subheader("🚩 Critical Risks Identified")
                    for clause in res.get('clauses', []):
                        explanation = clause.get('explanation_hindi') if is_hindi else clause.get('explanation_english')
                        with st.expander(f"⚠️ {explanation[:50]}..."):
                            st.markdown(f"**Analysis:** {explanation}")
                            st.markdown(f"**Original Text:** `{clause.get('original_text')}`")
                            st.markdown(f"**Recommendation:** {clause.get('recommendation')}")

    # ----------------------------------------------------
    # TAB 2: AI ASSISTANT (Chat with Contract) - NEW!
    # ----------------------------------------------------
    with tab2:
        st.markdown("### 🤖 Ask the Legal Assistant")
        st.caption("Ask specific questions about the uploaded contract (e.g., 'What is the notice period?', 'Is there a non-compete?').")

        if 'doc_text' in st.session_state:
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat history
            for message in st.session_state.messages:
                role_class = "chat-user" if message["role"] == "user" else "chat-ai"
                st.markdown(f"<div class='{role_class}'>{message['content']}</div>", unsafe_allow_html=True)

            # Chat Input
            if prompt := st.chat_input("Ask a question about this contract..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.markdown(f"<div class='chat-user'>{prompt}</div>", unsafe_allow_html=True)

                # Generate Answer
                with st.spinner("Analyzing document..."):
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    context = st.session_state['doc_text'][:30000] # Limit context
                    ai_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer based ONLY on the context above. Keep it legal but simple."
                    
                    try:
                        response = model.generate_content(ai_prompt)
                        ans = response.text
                    except:
                        ans = "I'm sorry, I couldn't process that request right now."

                # Add AI message
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
        else:
            st.warning("⚠️ Please upload a document in the 'Audit Dashboard' tab first.")

    # ----------------------------------------------------
    # TAB 3: CONTRACT DRAFTER
    # ----------------------------------------------------
    with tab3:
        st.markdown("### 📝 Smart Contract Drafter")
        c1, c2 = st.columns(2)
        with c1:
            doc_type = st.selectbox("Document Type", ["NDA", "Employment Agreement", "Freelance Contract", "Lease Deed"])
            p1 = st.text_input("Party 1 Name")
        with c2:
            loc = st.selectbox("Location", ["Delhi", "Mumbai", "Bangalore", "Hyderabad"])
            p2 = st.text_input("Party 2 Name")
            
        if st.button("Generate Draft"):
            if p1 and p2:
                with st.spinner("Drafting legal document..."):
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    d_prompt = f"Draft a professional {doc_type} between {p1} and {p2} for {loc}, India. Use clear professional legal language. Do NOT use markdown bolding (like **text**), use CAPITALIZATION for headers instead."
                    
                    try:
                        res = model.generate_content(d_prompt)
                        
                        # 1. Clean the text for display (Remove ** if AI still added them)
                        clean_draft = res.text.replace("**", "")
                        
                        # 2. Show in Text Area
                        st.text_area("Generated Draft", clean_draft, height=500)
                        
                        # 3. Import the new PDF generator function
                        from utils.helpers import generate_contract_pdf
                        
                        # 4. Create PDF
                        pdf_bytes = generate_contract_pdf(clean_draft)
                        
                        # 5. Download Button
                        st.download_button(
                            label="📄 Download Contract PDF",
                            data=pdf_bytes,
                            file_name=f"{doc_type.replace(' ', '_')}_Draft.pdf",
                            mime="application/pdf"
                        )
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please enter both Party Names to generate a contract.")

if __name__ == "__main__":
    main()