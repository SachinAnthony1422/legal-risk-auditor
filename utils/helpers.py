from fpdf import FPDF
import datetime

def clean_text(text):
    """
    Replaces characters that break PDF generation (like ₹) with safe alternatives.
    """
    if not isinstance(text, str):
        return str(text)
    
    # Replace Rupee symbol with 'Rs.' and fix smart quotes
    text = text.replace('\u20b9', 'Rs. ').replace('“', '"').replace('”', '"').replace('’', "'").replace('–', '-')
    
    # Force encode to ascii compatible latin-1, ignoring errors
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf_report(analysis_json, is_draft=True):
    """
    Generates the Risk Audit Report (Tab 1).
    """
    pdf = FPDF()
    pdf.add_page()
    
    # --- WATERMARK LOGIC (SAFE MODE) ---
    if is_draft:
        pdf.set_font("Arial", 'B', 60)
        pdf.set_text_color(230, 230, 230) # Very light gray
        pdf.cell(0, 30, "DRAFT COPY", ln=True, align='C')
        pdf.set_text_color(0, 0, 0) # Reset to black
        pdf.ln(10) 

    # --- Title Section ---
    pdf.set_font("Arial", 'B', 16)
    title = "LegalEagle AI - RISK ASSESSMENT REPORT"
    pdf.cell(0, 10, clean_text(title), ln=True, align='C')
    pdf.ln(5)
    
    # --- Meta Info ---
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, clean_text(f"Date Generated: {datetime.date.today()}"), ln=True)
    pdf.cell(0, 10, clean_text(f"Status: {'DRAFT - NOT FOR LEGAL USE' if is_draft else 'OFFICIAL REPORT'}"), ln=True)
    score = analysis_json.get('overall_score', 0)
    pdf.cell(0, 10, clean_text(f"Risk Score: {score}/100"), ln=True)
    pdf.ln(5)
    
    # --- Executive Summary ---
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, clean_text("Executive Summary:"), ln=True, fill=True)
    
    pdf.set_font("Arial", size=11)
    summary_text = analysis_json.get('summary_english', analysis_json.get('summary', 'No summary available.'))
    pdf.multi_cell(0, 8, clean_text(summary_text))
    pdf.ln(10)
    
    # --- Critical Risks ---
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, clean_text("Key Risk Analysis:"), ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    
    # FIX IS HERE: Changed 'analysis' to 'analysis_json'
    for clause in analysis_json.get('clauses', []):
        risk_score = clause.get('risk_score', 0)
        if risk_score > 75:
            pdf.set_text_color(200, 0, 0)
        else:
            pdf.set_text_color(200, 120, 0)
            
        pdf.set_font("Arial", 'B', 10)
        explanation = clause.get('explanation_english', clause.get('explanation', ''))
        pdf.cell(0, 8, clean_text(f"FLAG: {explanation[:60]}... (Score: {risk_score})"), ln=True)
        pdf.set_text_color(0, 0, 0)
        
        pdf.set_font("Arial", 'I', 9)
        pdf.multi_cell(0, 5, clean_text(f"Original: {clause.get('original_text', '')}"))
        
        pdf.set_font("Arial", 'B', 9)
        rec = clause.get('recommendation', 'No specific recommendation.')
        pdf.multi_cell(0, 5, clean_text(f"Advice: {rec}"))
        pdf.ln(5)
        
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- FUNCTION FOR TAB 3 ---
def generate_contract_pdf(contract_text):
    """
    Generates a clean Contract PDF (Tab 3).
    Removes Markdown, handles formatting.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "LEGAL AGREEMENT", ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=11)
    
    # Process text line by line
    for line in contract_text.split('\n'):
        # Clean Markdown bolding (**)
        clean_line = line.replace('**', '').strip()
        
        if not clean_line:
            pdf.ln(5) # Add space for empty lines
            continue
            
        # Check if it's a Header (Usually uppercase or starts with Number)
        # We simulate bolding for headers
        if clean_line.isupper() or (len(clean_line) < 50 and clean_line.endswith(':')):
            pdf.set_font("Arial", 'B', 11)
            pdf.multi_cell(0, 6, clean_text(clean_line))
            pdf.set_font("Arial", size=11) # Reset to normal
        else:
            pdf.multi_cell(0, 6, clean_text(clean_line))
            
    return pdf.output(dest='S').encode('latin-1', 'ignore')