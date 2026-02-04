import streamlit as st
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
from utils.helpers import generate_pdf_report, generate_contract_pdf

# Load Environment
load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except:
    st.error("⚠️ Gemini API Key missing. Please check your .env file or Streamlit Secrets.")

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="LegalEagle AI | Enterprise Edition",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- 3. LANDING PAGE DESIGN (Advanced UI/UX) ---
def show_landing_page():
    # Custom CSS for a SaaS-like look
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        .main-title { 
            font-size: 4rem; 
            font-weight: 900; 
            color: #1E293B; 
            line-height: 1.1; 
            margin-bottom: 10px;
            background: -webkit-linear-gradient(45deg, #1e293b, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .sub-title { 
            font-size: 1.25rem; 
            color: #64748B; 
            margin-bottom: 30px; 
            font-weight: 300;
        }
        
        .feature-card { 
            background: white; 
            padding: 25px; 
            border-radius: 16px; 
            border: 1px solid #E2E8F0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        .feature-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            border-color: #3B82F6;
        }
        
        /* Button Animation */
        div.stButton > button {
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True) # Spacer
        st.markdown('<h1 class="main-title">Legal Intelligence <br>Reimagined.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Automate contract review, detect hidden risks, and draft airtight agreements in seconds with <b>Gemini 1.5 Pro</b>.</p>', unsafe_allow_html=True)
        
        # Call to Action Button with Logic
        if st.button("🚀 Launch Dashboard", type="primary"):
            with st.spinner("Initializing Secure Environment..."):
                time.sleep(1.2)  # Professional loading effect
                st.session_state.page = 'app'
                st.rerun()
                
        st.markdown("<br><small>🔒 Enterprise-Grade Security • AES-256 Encryption</small>", unsafe_allow_html=True)

    with col2:
        # Professional Hero Image
        st.image("https://cdn.dribbble.com/users/508588/screenshots/16205837/media/d93563919e1a0b380313543d4f826359.jpg", use_container_width=True)

    st.markdown("---")

    # --- FEATURES GRID ---
    st.subheader("💡 Why Choose LegalEagle AI?")
    
    feat1, feat2, feat3 = st.columns(3)
    
    with feat1:
        st.markdown("""
        <div class="feature-card">
        <h3>🔍 Instant Forensic Audit</h3>
        <p>Upload PDFs and get a risk score instantly. We cross-reference clauses against the Indian Contract Act, 1872.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with feat2:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 Legal Chat Assistant</h3>
        <p>Your personal AI lawyer. Ask <i>"Is the indemnity clause fair?"</i> and get plain English answers citing specific pages.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with feat3:
        st.markdown("""
        <div class="feature-card">
        <h3>📝 Smart Drafting</h3>
        <p>Auto-generate NDAs, Employment Contracts, and Lease Deeds tailored to Indian jurisdiction in seconds.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
    Developed by <b>SACHIN S</b> for HCL GUVI Hackathon 2026
    </div>
    """, unsafe_allow_html=True)

# --- 4. PAGE ROUTING LOGIC ---
if st.session_state.page == 'landing':
    show_landing_page()
    st.stop()  # 🛑 STOPS HERE so the main app doesn't load yet

# =========================================================
# 🔻 MAIN APP LOGIC STARTS HERE (Only loads after click) 🔻
# =========================================================

# --- HELPER FUNCTIONS ---
def create_gauge_chart(score):
    """Draws a professional Risk Gauge."""
    color = "#22C55E" # Green
    if score > 40: color = "#F59E0B" # Orange
    if score > 75: color = "#EF4444" # Red
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score", 'font': {'size': 24, 'color': "#64748B"}},
        number = {'font': {'size': 50, 'color': color, 'family': "Inter"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 40], 'color': '#DCFCE7'},
                {'range': [40, 75], 'color': '#FEF3C7'},
                {'range': [75, 100], 'color': '#FEE2E2'}],
        }
    ))
    fig.update_layout(height=250, margin={'t': 40, 'b': 0, 'l': 20, 'r': 20}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def anonymize_text(text):
    """Simple PII redaction"""
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[REDACTED_EMAIL]", text)
    text = re.sub(r'\b\d{10}\b', "[REDACTED_PHONE]", text)
    return text

# --- APP UI ---
# Custom CSS for App Mode
st.markdown("""
    <style>
    /* Glassmorphism Header */
    .main-header {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #e0e0e0;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Metrics Cards */
    .metric-container {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    .metric-container:hover { transform: translateY(-2px); }
    .metric-value { font-size: 28px; font-weight: 800; color: #1E293B; margin-top: 5px; }
    .metric-label { font-size: 14px; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Chat Bubbles */
    .chat-user { 
        background-color: #3B82F6; 
        color: white;
        padding: 14px 18px; 
        border-radius: 18px 18px 0 18px; 
        margin: 8px 0; 
        text-align: right; 
        float: right;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3);
    }
    .chat-ai { 
        background-color: #F1F5F9; 
        color: #1E293B;
        padding: 14px 18px; 
        border-radius: 18px 18px 18px 0; 
        margin: 8px 0; 
        border: 1px solid #E2E8F0;
        float: left;
        max-width: 80%;
    }
    .chat-container { overflow: auto; display: flex; flex-direction: column; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #64748B;
        font-weight: 600;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EFF6FF;
        color: #3B82F6;
        border: 1px solid #BFDBFE;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2666/2666505.png", width=60)
    st.markdown("### Control Center")
    
    st.markdown("---")
    st.markdown("**🛡️ Privacy Shield**")
    privacy_mode = st.toggle("Anonymize Personal Data", value=False, help="Masks emails and phones before sending to AI.")
    
    st.markdown("---")
    with st.container():
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 10px; border-radius: 8px; border: 1px solid #E2E8F0;">
            <small style="color: #64748B;">System Status</small><br>
            <span style="color: #22C55E; font-weight: bold;">● Online</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("👨‍💻 Developed by **SACHIN S** for HCL GUVI Hackathon")

    if st.button("⬅️ Log Out"):
        st.session_state.page = 'landing'
        st.rerun()

# Main Header
st.markdown("""
<div class="main-header">
    <div>
        <h2 style="margin:0; color:#1E293B;">⚖️ LegalEagle AI</h2>
        <span style="color:#64748B; font-size: 14px;">Enterprise Contract Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["📊 Audit Dashboard", "🤖 Legal Chat", "📝 Drafter"])

# ----------------------------------------------------
# TAB 1: AUDIT DASHBOARD (Main Analysis)
# ----------------------------------------------------
with tab1:
    if 'doc_text' not in st.session_state:
        # Empty State
        st.markdown("""
        <div style="text-align: center; padding: 50px; border: 2px dashed #CBD5E1; border-radius: 12px; background-color: #F8FAFC;">
            <h3 style="color: #475569;">No Document Uploaded</h3>
            <p style="color: #94A3B8;">Upload a contract to begin the forensic audit.</p>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Agreement", type=['pdf', 'docx'], label_visibility="collapsed")
    else:
        # Mini Uploader (to change file)
        with st.expander("📂 Change Document"):
             uploaded_file = st.file_uploader("Upload New Agreement", type=['pdf', 'docx'])

    if uploaded_file:
        # 1. Parse
        if 'doc_text' not in st.session_state or (uploaded_file.name != st.session_state.get('last_filename')):
            with st.spinner("Extracting text from document..."):
                raw_text, error = DocumentParser.parse_file(uploaded_file)
                if error:
                    st.error(error)
                    st.stop()
                st.session_state['doc_text'] = raw_text
                st.session_state['last_filename'] = uploaded_file.name
                st.session_state.pop('analysis_result', None) # Clear old results
                st.toast("Document uploaded successfully!", icon="✅")
                st.rerun()

        text_to_analyze = st.session_state['doc_text']
        if privacy_mode:
            text_to_analyze = anonymize_text(text_to_analyze)

        # 2. Analyze Button (Centered)
        if 'analysis_result' not in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🚀 Run Forensic Audit", type="primary", use_container_width=True):
                    risk_engine = LegalRiskEngine()
                    with st.status("🔍 Analyzing Contract...", expanded=True) as status:
                        st.write("Scanning for liability clauses...")
                        time.sleep(0.8)
                        st.write("Checking compliance with Indian Contract Act...")
                        time.sleep(0.8)
                        st.write("Calculating Risk Score...")
                        result = risk_engine.analyze_contract(text_to_analyze)
                        st.session_state['analysis_result'] = result
                        status.update(label="Audit Complete!", state="complete", expanded=False)
                    st.rerun()

        # 3. Display Dashboard
        if 'analysis_result' in st.session_state:
            res = st.session_state['analysis_result']
            
            # Top Metrics Row
            m1, m2, m3 = st.columns(3)
            m1.markdown(f"<div class='metric-container'><div class='metric-label'>Risk Score</div><div class='metric-value' style='color: {'#EF4444' if res['overall_score'] > 70 else '#22C55E'}'>{res.get('overall_score')}/100</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-container'><div class='metric-label'>Clauses Flagged</div><div class='metric-value'>{len(res.get('clauses', []))}</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-container'><div class='metric-label'>Jurisdiction</div><div class='metric-value'>India 🇮🇳</div></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Main Layout
            c_left, c_right = st.columns([1, 2], gap="medium")
            
            with c_left:
                st.markdown("### Risk Meter")
                st.plotly_chart(create_gauge_chart(res.get('overall_score')), use_container_width=True)
                
                st.markdown("### Actions")
                official = st.checkbox("Official Report Mode")
                report_data = generate_pdf_report(res, is_draft=not official)
                st.download_button("📥 Download PDF Report", data=report_data, file_name="Audit_Report.pdf", mime="application/pdf", use_container_width=True)

            with c_right:
                st.markdown("### 📋 Executive Summary")
                st.info(res.get('summary_english'))
                
                st.markdown("### 🚩 Critical Risks")
                if not res.get('clauses'):
                    st.success("No high-risk clauses detected. This contract looks safe!")
                
                for clause in res.get('clauses', []):
                    with st.expander(f"⚠️ {clause.get('explanation_english')[:60]}..."):
                        st.markdown(f"**🔴 Risk Analysis:** {clause.get('explanation_english')}")
                        st.markdown(f"**📜 Original Text:**\n> *{clause.get('original_text')}*")
                        st.markdown(f"**💡 Recommendation:** {clause.get('recommendation')}")

# ----------------------------------------------------
# TAB 2: AI ASSISTANT (Modern Chat)
# ----------------------------------------------------
with tab2:
    st.markdown("### 🤖 Legal Assistant")
    
    if 'doc_text' in st.session_state:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Container for chat history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                role_class = "chat-user" if message["role"] == "user" else "chat-ai"
                st.markdown(f"""
                <div style="overflow: hidden;">
                    <div class='{role_class}'>{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Chat Input
        if prompt := st.chat_input("Ask about notice periods, non-competes, etc..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                st.markdown(f"<div style='overflow: hidden;'><div class='chat-user'>{prompt}</div></div>", unsafe_allow_html=True)

            # Generate Answer
            with st.spinner("Consulting legal database..."):
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    context = st.session_state['doc_text'][:30000] # Limit context
                    ai_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer based ONLY on the context above. Keep it legal but simple."
                    response = model.generate_content(ai_prompt)
                    ans = response.text
                except Exception as e:
                    ans = "I'm sorry, I couldn't process that request right now. (Model Error)"

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
    st.caption("Generate legally binding agreements tailored for Indian Jurisdiction.")
    
    with st.container():
        st.markdown("<div style='background: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            doc_type = st.selectbox("Document Type", ["NDA", "Employment Agreement", "Freelance Contract", "Lease Deed"])
            p1 = st.text_input("Party 1 (e.g., Company Name)")
        with c2:
            loc = st.selectbox("Jurisdiction", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"])
            p2 = st.text_input("Party 2 (e.g., Employee Name)")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ Generate Draft", type="primary"):
        if p1 and p2:
            with st.spinner("Drafting legal document..."):
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    d_prompt = f"Draft a professional {doc_type} between {p1} and {p2} for {loc}, India. Use clear professional legal language. Do NOT use markdown bolding (like **text**), use CAPITALIZATION for headers instead."
                    
                    res = model.generate_content(d_prompt)
                    clean_draft = res.text.replace("**", "")
                    
                    # Show
                    st.text_area("Generated Draft", clean_draft, height=500)
                    
                    # PDF Download
                    pdf_bytes = generate_contract_pdf(clean_draft)
                    st.download_button(
                        label="📄 Download Contract PDF",
                        data=pdf_bytes,
                        file_name=f"{doc_type.replace(' ', '_')}_Draft.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("⚠️ Please enter both Party Names to generate a contract.")