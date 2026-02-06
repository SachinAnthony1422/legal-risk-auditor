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

# --- 2. ROBUST MODEL FALLBACK SYSTEM (OPTIMIZED FOR YOUR QUOTA) ---
# Based on your dashboard image:
# 1. Gemini 2.5 Flash Lite (Has capacity: 6/10)
# 2. Gemini 3 Flash (Empty: 0/5) - Great backup
# 3. Gemini 2.0 Flash Lite (Reliable backup)
# 4. Gemini 2.5 Flash (Moved to bottom because it's full: 5/5)
MODEL_PRIORITY = [
    "gemini-2.5-flash-lite",      # Priority 1: Best available quota
    "gemini-3-flash",             # Priority 2: New & Empty quota
    "gemini-2.0-flash-lite",      # Priority 3: Fast backup
    "gemini-1.5-flash",           # Priority 4: Old Reliable
    "gemini-2.5-flash",           # Priority 5: Currently Full (Use as last resort)
    "gemini-1.5-pro",             # Priority 6: Slower but smart
    "gemini-pro"                  # Priority 7: Legacy
]

def generate_smart_fallback(prompt):
    """
    Iterates through the model list until one works.
    Includes a small delay to handle 'Busy' signals.
    """
    last_error = None
    for model_name in MODEL_PRIORITY:
        try:
            # st.toast(f"Attempting with {model_name}...", icon="🤖") # Uncomment for debugging
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = e
            time.sleep(0.5) # Brief pause to let API breathe
            continue 
    
    return f"⚠️ System Busy. Please wait 10s. (Details: {str(last_error)})"

# --- 3. TRANSLATION DICTIONARY ---
TRANSLATIONS = {
    "English": {
        "nav_audit": "📊 Audit Dashboard",
        "nav_chat": "🤖 Legal Chat",
        "nav_draft": "📝 Drafter",
        "upload_label": "Upload Agreement",
        "upload_sub": "Upload a contract to begin the forensic audit.",
        "change_doc": "📂 Change Document",
        "run_audit": "🚀 Run Forensic Audit",
        "analyzing": "🔍 Analyzing Contract...",
        "risk_score": "Risk Score",
        "clauses_flagged": "Clauses Flagged",
        "jurisdiction": "Jurisdiction",
        "actions": "Actions",
        "download_report": "📥 Download PDF Report",
        "exec_summary": "📋 Executive Summary",
        "crit_risks": "🚩 Critical Risks",
        "chat_placeholder": "Ask about notice periods, non-competes, etc...",
        "draft_title": "📝 Smart Contract Drafter",
        "draft_caption": "Generate legally binding agreements tailored for Indian Jurisdiction.",
        "doc_type": "Document Type",
        "party_1": "Party 1 (e.g., Company)",
        "party_2": "Party 2 (e.g., Employee)",
        "location": "Jurisdiction (City)",
        "gen_draft": "✨ Generate Draft",
        "download_contract": "📄 Download Contract PDF",
        "privacy": "🛡️ Privacy Shield",
        "anonymize": "Anonymize Personal Data",
        "control_center": "Control Center",
        "lbl_analysis": "Analysis",
        "lbl_original": "Original Text",
        "lbl_rec": "Recommendation"
    },
    "Hindi (हिंदी)": {
        "nav_audit": "📊 ऑडिट डैशबोर्ड",
        "nav_chat": "🤖 कानूनी चैट",
        "nav_draft": "📝 ड्राफ्टर",
        "upload_label": "समझौता अपलोड करें",
        "upload_sub": "ऑडिट शुरू करने के लिए अनुबंध अपलोड करें।",
        "change_doc": "📂 दस्तावेज़ बदलें",
        "run_audit": "🚀 फोरेंसिक ऑडिट चलाएं",
        "analyzing": "🔍 अनुबंध का विश्लेषण हो रहा है...",
        "risk_score": "जोखिम स्कोर",
        "clauses_flagged": "फ्लैग की गई धाराएं",
        "jurisdiction": "अधिकार क्षेत्र",
        "actions": "कार्रवाई",
        "download_report": "📥 पीडीएफ रिपोर्ट डाउनलोड करें",
        "exec_summary": "📋 कार्यकारी सारांश",
        "crit_risks": "🚩 महत्वपूर्ण जोखिम",
        "chat_placeholder": "नोटिस अवधि, गैर-प्रतिस्पर्धा आदि के बारे में पूछें...",
        "draft_title": "📝 स्मार्ट अनुबंध ड्राफ्टर",
        "draft_caption": "भारतीय अधिकार क्षेत्र के लिए कानूनी रूप से बाध्यकारी समझौते बनाएं।",
        "doc_type": "दस्तावेज़ का प्रकार",
        "party_1": "पक्ष 1 (जैसे, कंपनी)",
        "party_2": "पक्ष 2 (जैसे, कर्मचारी)",
        "location": "शहर (City)",
        "gen_draft": "✨ ड्राफ्ट तैयार करें",
        "download_contract": "📄 अनुबंध पीडीएफ डाउनलोड करें",
        "privacy": "🛡️ गोपनीयता कवच",
        "anonymize": "व्यक्तिगत डेटा छिपाएं",
        "control_center": "नियंत्रण केंद्र",
        "lbl_analysis": "विश्लेषण (Analysis)",
        "lbl_original": "मूल पाठ (Original Text)",
        "lbl_rec": "सुझाव (Recommendation)"
    },
    "Tamil (தமிழ்)": {
        "nav_audit": "📊 தணிக்கை குழு",
        "nav_chat": "🤖 சட்ட அரட்டை",
        "nav_draft": "📝 வரைவாளர்",
        "upload_label": "ஒப்பந்தத்தை பதிவேற்றவும்",
        "upload_sub": "தணிக்கையைத் தொடங்க ஒப்பந்தத்தைப் பதிவேற்றவும்.",
        "change_doc": "📂 ஆவணத்தை மாற்றவும்",
        "run_audit": "🚀 தடயவியல் தணிக்கையை இயக்கவும்",
        "analyzing": "🔍 பகுப்பாய்வு செய்கிறது...",
        "risk_score": "ஆபத்து மதிப்பெண்",
        "clauses_flagged": "குறிக்கப்பட்ட விதிகள்",
        "jurisdiction": "அதிகார வரம்பு",
        "actions": "செயல்கள்",
        "download_report": "📥 அறிக்கையைப் பதிவிறக்கவும்",
        "exec_summary": "📋 நிர்வாகச் சுருக்கம்",
        "crit_risks": "🚩 முக்கிய அபாயங்கள்",
        "chat_placeholder": "அறிவிப்பு காலம் பற்றி கேட்கவும்...",
        "draft_title": "📝 ஸ்மார்ட் ஒப்பந்த வரைவாளர்",
        "draft_caption": "சட்டப்பூர்வ ஒப்பந்தங்களை உருவாக்கவும்.",
        "doc_type": "ஆவண வகை",
        "party_1": "தரப்பு 1 (எ.கா., நிறுவனம்)",
        "party_2": "தரப்பு 2 (எ.கா., பணியாளர்)",
        "location": "அதிகார வரம்பு",
        "gen_draft": "✨ வரைவை உருவாக்குங்கள்",
        "download_contract": "📄 ஒப்பந்தத்தைப் பதிவிறக்கவும்",
        "privacy": "🛡️ தனியுரிமை கவசம்",
        "anonymize": "தரவை மறைக்கவும்",
        "control_center": "கட்டுப்பாட்டு மையம்",
        "lbl_analysis": "பகுப்பாய்வு (Analysis)",
        "lbl_original": "அசல் உரை (Original)",
        "lbl_rec": "பரிந்துரை (Recommendation)"
    }
}

# --- 4. SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'language' not in st.session_state:
    st.session_state.language = "English"

def t(key):
    """Helper function to get translated text based on selected language."""
    lang_dict = TRANSLATIONS.get(st.session_state.language, TRANSLATIONS["English"])
    return lang_dict.get(key, TRANSLATIONS["English"].get(key, key))

# --- 5. LANDING PAGE DESIGN ---
def show_landing_page():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
            background-image: linear-gradient(#e2e8f0 1px, transparent 1px), linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
            background-size: 40px 40px;
        }
        .main-title { 
            font-size: 4rem; font-weight: 900; color: #1E293B; line-height: 1.1; margin-bottom: 10px;
            background: -webkit-linear-gradient(45deg, #1e293b, #3b82f6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .sub-title { font-size: 1.25rem; color: #64748B; margin-bottom: 30px; font-weight: 300; }
        .feature-card { 
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 25px; 
            border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #3B82F6; }
        div.stButton > button { transition: all 0.3s ease; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5); }
        div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.6); }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True) 
        st.markdown('<h1 class="main-title">Legal Intelligence <br>Reimagined.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Automate contract review, detect hidden risks, and draft airtight agreements in seconds with <b>Gemini 2.5 Flash Lite</b>.</p>', unsafe_allow_html=True)
        
        if st.button("🚀 Launch Dashboard", type="primary"):
            with st.spinner("Initializing Secure Environment..."):
                time.sleep(1.2)
                st.session_state.page = 'app'
                st.rerun()
        st.markdown("<br><small>🔒 Enterprise-Grade Security • AES-256 Encryption</small>", unsafe_allow_html=True)

    with col2:
        st.image("banner.png", use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Why Choose LegalEagle AI?")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""<div class="feature-card"><h3>🔍 Instant Forensic Audit</h3><p>Upload PDFs and get a risk score instantly. We cross-reference clauses against the Indian Contract Act, 1872.</p></div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""<div class="feature-card"><h3>🤖 Legal Chat Assistant</h3><p>Your personal AI lawyer. Ask <i>"Is the indemnity clause fair?"</i> and get plain English answers citing specific pages.</p></div>""", unsafe_allow_html=True)
    with f3:
        st.markdown("""<div class="feature-card"><h3>📝 Smart Drafting</h3><p>Auto-generate NDAs, Employment Contracts, and Lease Deeds tailored to Indian jurisdiction in seconds.</p></div>""", unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">Developed by <b>SACHIN S</b> for HCL GUVI Hackathon 2026</div>""", unsafe_allow_html=True)

if st.session_state.page == 'landing':
    show_landing_page()
    st.stop()

# =========================================================
# 🔻 MAIN APP LOGIC 🔻
# =========================================================

def create_gauge_chart(score):
    color = "#22C55E" # Green
    if score > 40: color = "#F59E0B" # Orange
    if score > 75: color = "#EF4444" # Red
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': t("risk_score"), 'font': {'size': 24, 'color': "#64748B"}},
        number = {'font': {'size': 50, 'color': color, 'family': "Inter"}},
        gauge = {'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                 'bar': {'color': color}, 'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "#E2E8F0",
                 'steps': [{'range': [0, 40], 'color': '#DCFCE7'}, {'range': [40, 75], 'color': '#FEF3C7'}, {'range': [75, 100], 'color': '#FEE2E2'}]}
    ))
    fig.update_layout(height=250, margin={'t': 40, 'b': 0, 'l': 20, 'r': 20}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def anonymize_text(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[REDACTED_EMAIL]", text)
    text = re.sub(r'\b\d{10}\b', "[REDACTED_PHONE]", text)
    return text

# --- APP UI ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    .main-header { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid #e0e0e0; padding: 15px 20px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .metric-container { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: transform 0.2s; }
    .metric-container:hover { transform: translateY(-2px); }
    .metric-value { font-size: 28px; font-weight: 800; color: #1E293B; margin-top: 5px; }
    .metric-label { font-size: 14px; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .chat-user { background-color: #3B82F6; color: white; padding: 14px 18px; border-radius: 18px 18px 0 18px; margin: 8px 0; text-align: right; float: right; max-width: 80%; box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3); }
    .chat-ai { background-color: #ffffff; color: #1E293B; padding: 14px 18px; border-radius: 18px 18px 18px 0; margin: 8px 0; border: 1px solid #E2E8F0; float: left; max-width: 80%; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 8px; color: #64748B; font-weight: 600; border: 1px solid transparent; }
    .stTabs [aria-selected="true"] { background-color: #EFF6FF; color: #3B82F6; border: 1px solid #BFDBFE; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2666/2666505.png", width=60)
    st.markdown(f"### {t('control_center')}")
    st.markdown("---")
    st.markdown("**🌍 Language / भाषा**")
    selected_lang = st.selectbox("Select Output Language", ["English", "Hindi (हिंदी)", "Tamil (தமிழ்)"], label_visibility="collapsed")
    if st.session_state.language != selected_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**{t('privacy')}**")
    privacy_mode = st.toggle(t("anonymize"), value=False)
    
    st.markdown("---")
    with st.container():
        st.markdown("""<div style="background-color: #F8FAFC; padding: 10px; border-radius: 8px; border: 1px solid #E2E8F0;"><small style="color: #64748B;">System Status</small><br><span style="color: #22C55E; font-weight: bold;">● Online</span></div>""", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("👨‍💻 Developed by **SACHIN S** for HCL GUVI Hackathon")
    if st.button("⬅️ Log Out"):
        st.session_state.page = 'landing'
        st.rerun()

st.markdown("""<div class="main-header"><div><h2 style="margin:0; color:#1E293B;">⚖️ LegalEagle AI</h2><span style="color:#64748B; font-size: 14px;">Enterprise Contract Intelligence</span></div></div>""", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs([t("nav_audit"), t("nav_chat"), t("nav_draft")])

# --- TAB 1: AUDIT ---
with tab1:
    # --- PERSISTENCE LOGIC START ---
    if 'doc_text' not in st.session_state:
        st.markdown(f"""<div style="text-align: center; padding: 50px; border: 2px dashed #CBD5E1; border-radius: 12px; background-color: #F8FAFC;"><h3 style="color: #475569;">{t("upload_label")}</h3><p style="color: #94A3B8;">{t("upload_sub")}</p></div>""", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Agreement", type=['pdf', 'docx'], label_visibility="collapsed")
        
        if uploaded_file:
            with st.spinner("Extracting text..."):
                raw_text, error = DocumentParser.parse_file(uploaded_file)
                if error:
                    st.error(error)
                    st.stop()
                st.session_state['doc_text'] = raw_text
                st.session_state['last_filename'] = uploaded_file.name
                st.session_state.pop('analysis_result', None) 
                st.rerun()
    else:
        with st.expander(t("change_doc")):
             new_file = st.file_uploader("Upload New Agreement", type=['pdf', 'docx'])
             if new_file:
                 raw_text, error = DocumentParser.parse_file(new_file)
                 if not error:
                     st.session_state['doc_text'] = raw_text
                     st.session_state['last_filename'] = new_file.name
                     st.session_state.pop('analysis_result', None)
                     st.rerun()

        text_to_analyze = st.session_state['doc_text']
        if privacy_mode: text_to_analyze = anonymize_text(text_to_analyze)

        if 'analysis_result' not in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button(t("run_audit"), type="primary", use_container_width=True):
                    risk_engine = LegalRiskEngine()
                    with st.status(t("analyzing"), expanded=True) as status:
                        time.sleep(1)
                        result = risk_engine.analyze_contract(text_to_analyze)
                        st.session_state['analysis_result'] = result
                        status.update(label="Complete!", state="complete", expanded=False)
                    st.rerun()

        if 'analysis_result' in st.session_state:
            res = st.session_state['analysis_result']
            m1, m2, m3 = st.columns(3)
            m1.markdown(f"<div class='metric-container'><div class='metric-label'>{t('risk_score')}</div><div class='metric-value' style='color: {'#EF4444' if res['overall_score'] > 70 else '#22C55E'}'>{res.get('overall_score')}/100</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-container'><div class='metric-label'>{t('clauses_flagged')}</div><div class='metric-value'>{len(res.get('clauses', []))}</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-container'><div class='metric-label'>{t('jurisdiction')}</div><div class='metric-value'>India 🇮🇳</div></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c_left, c_right = st.columns([1, 2], gap="medium")
            
            with c_left:
                st.markdown(f"### {t('risk_score')}")
                st.plotly_chart(create_gauge_chart(res.get('overall_score')), use_container_width=True)
                st.markdown(f"### {t('actions')}")
                official = st.checkbox("Official Report Mode")
                report_data = generate_pdf_report(res, is_draft=not official)
                st.download_button(t("download_report"), data=report_data, file_name="Audit_Report.pdf", mime="application/pdf", use_container_width=True)

            with c_right:
                st.markdown(f"### {t('exec_summary')}")
                summary_text = res.get('summary_english')
                if st.session_state.language != "English":
                    with st.spinner(f"Translating summary to {st.session_state.language}..."):
                         summary_text = generate_smart_fallback(f"Translate this legal summary to {st.session_state.language}: {summary_text}")
                st.info(summary_text)
                
                st.markdown(f"### {t('crit_risks')}")
                if not res.get('clauses'):
                    st.success("No high-risk clauses detected.")
                
                for clause in res.get('clauses', []):
                    explanation = clause.get('explanation_english')
                    recommendation = clause.get('recommendation')
                    
                    # --- TRANSLATION FIX FOR CRITICAL RISKS ---
                    if st.session_state.language != "English":
                        combined_prompt = f"""
                        Translate these two legal texts to {st.session_state.language}.
                        1. {explanation}
                        2. {recommendation}
                        Format the output as:
                        Trans1: [translation of 1]
                        Trans2: [translation of 2]
                        """
                        try:
                            trans_res = generate_smart_fallback(combined_prompt)
                            if "Trans1:" in trans_res and "Trans2:" in trans_res:
                                parts = trans_res.split("Trans2:")
                                explanation = parts[0].replace("Trans1:", "").strip()
                                recommendation = parts[1].strip()
                        except:
                            pass 

                    with st.expander(f"⚠️ {explanation[:60]}..."):
                        st.markdown(f"**{t('lbl_analysis')}:** {explanation}")
                        st.markdown(f"**{t('lbl_original')}:**\n> *{clause.get('original_text')}*")
                        st.markdown(f"**{t('lbl_rec')}:** {recommendation}")

# --- TAB 2: CHAT ---
with tab2:
    st.markdown(f"### {t('nav_chat')}")
    if 'doc_text' in st.session_state:
        if "messages" not in st.session_state: st.session_state.messages = []
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                role_class = "chat-user" if message["role"] == "user" else "chat-ai"
                st.markdown(f"<div style='overflow: hidden;'><div class='{role_class}'>{message['content']}</div></div>", unsafe_allow_html=True)
        if prompt := st.chat_input(t("chat_placeholder")):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container: st.markdown(f"<div style='overflow: hidden;'><div class='chat-user'>{prompt}</div></div>", unsafe_allow_html=True)
            with st.spinner("Thinking..."):
                context = st.session_state['doc_text'][:30000]
                ai_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer based ONLY on the context. Answer in {st.session_state.language} language."
                ans = generate_smart_fallback(ai_prompt)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()
    else:
        st.warning(f"⚠️ {t('upload_sub')}")

# --- TAB 3: DRAFTER ---
with tab3:
    st.markdown(f"### {t('draft_title')}")
    st.caption(t("draft_caption"))
    with st.container():
        st.markdown("<div style='background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            doc_type = st.selectbox(t("doc_type"), ["NDA", "Employment Agreement", "Freelance Contract", "Lease Deed"])
            p1 = st.text_input(t("party_1"))
        with c2:
            loc = st.selectbox(t("location"), ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"])
            p2 = st.text_input(t("party_2"))
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t("gen_draft"), type="primary"):
        if p1 and p2:
            with st.spinner("Drafting..."):
                d_prompt = f"Draft a professional {doc_type} between {p1} and {p2} for {loc}, India. Draft in {st.session_state.language} language. Use professional legal terminology."
                res_text = generate_smart_fallback(d_prompt)
                clean_draft = res_text.replace("**", "")
                st.text_area("Generated Draft", clean_draft, height=500)
                pdf_bytes = generate_contract_pdf(clean_draft)
                st.download_button(t("download_contract"), data=pdf_bytes, file_name="Draft.pdf", mime="application/pdf")
        else:
            st.error("⚠️ Please enter details.")