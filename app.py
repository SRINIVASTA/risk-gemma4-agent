# ==========================================
# ─── APP BLOCK 1: INITIALIZATION & OPERATIONAL TERMINAL (TAB 1) ───
# ==========================================
import streamlit as st
import os
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Risk-Gemma4-Agent Panel", page_icon="🛡️", layout="wide")

# ─── 🔑 AUTHENTICATION LAYER ───
st.sidebar.header("🔑 Authentication")
user_key = st.sidebar.text_input(
    "Enter Google API Key", 
    type="password", 
    help="Provide your Gemini API Key from Google AI Studio. It is safely isolated in session memory."
)

if user_key:
    if st.session_state.get("active_key") != user_key:
        st.session_state["active_key"] = user_key
        st.cache_resource.clear()
    os.environ["GOOGLE_API_KEY"] = user_key

if not os.environ.get("GOOGLE_API_KEY"):
    st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
    st.info("💡 **Welcome to the Workspace!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemma 4 pipelines.")
    st.stop()

from gemma4_engine import FraudCopilotEngine

@st.cache_resource
def init_engine():
    return FraudCopilotEngine()

try:
    engine = init_engine()
except Exception as e:
    st.error(f"❌ Initialization Error: {e}")
    st.stop()

# ─── 🎛️ DYNAMIC SIDEBAR CONTROL PANEL ───
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")

def handle_threshold_shift():
    if "audit_data_cache" in st.session_state:
        del st.session_state["audit_data_cache"]

if "current_threshold" not in st.session_state:
    st.session_state["current_threshold"] = 5000000

min_threshold = st.sidebar.slider(
    "Cross-Border Alert Threshold (₹)", 
    1000000, 10000000, 
    key="current_threshold",
    step=500000,
    on_change=handle_threshold_shift
)

# ─── 🧠 REASONING ENGINE CONFIGURATION HUB ───
st.sidebar.markdown("---")
st.sidebar.header("🧠 Reasoning Engine Layout")

# Map user-friendly dropdown options to strings expected by the Google SDK client
thinking_options = {
    "⚡ Minimal (Fastest / Direct)": "minimal",
    "🟢 Low (Calibrated Balance)": "low",
    "🟡 Medium (Deep Processing)": "medium",
    "🔴 High (Full Reasoning Cluster)": "high"
}

selected_label = st.sidebar.selectbox(
    "Gemma 4 Thinking Tier:",
    list(thinking_options.keys()),
    index=0,  # Defaults to Minimal for optimized immediate response delivery speeds
    help="Higher tiers activate deep model-level reasoning but increase server processing latency."
)

# Store the active selected parameter safely in session state memory logs
st.session_state["active_thinking_level"] = thinking_options[selected_label]

# ─── 📁 DASHBOARD STATE & TAB INITIALIZATION ───
if "messages" not in st.session_state:
    st.session_state.messages = []

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Operational Dashboard", 
    "💬 Conversational CoCo Copilot", 
    "📁 Account Directory Lookup",
    "🛠️ Remediation & Actions Console"
])

with tab1:
    st.header("🛡️ Risk & Compliance Monitoring Terminal")
    st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")
    
    if st.button("Run Global Compliance Audit Pipeline", type="primary"):
        st.subheader("✅ Step 1: Signal Detection (Structured Data)")
        signals_df = engine.detect_signals(min_amount=min_threshold)
        
        if signals_df.empty:
            st.warning("No anomalies detected for this configuration threshold.")
        else:
            total_incidents = len(signals_df)
            st.success(f"Detected {total_incidents} matching high-risk account profiles.")
            
            signals_df.columns = signals_df.columns.str.strip().str.upper()
            total_flagged_amt = int(signals_df["AMOUNT"].sum())
            avg_risk_score = float(signals_df["RISK_SCORE"].mean())
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label="🚨 Flagged Incidents Count", value=f"{total_incidents} Signals")
            col2.metric(label="💰 Total Capital Exposure", value=f"₹{total_flagged_amt:,}")
            col3.metric(label="⚠️ Average Network Risk Factor", value=f"{avg_risk_score:.1f}%")
            
            st.dataframe(signals_df, use_container_width=True)
            
            try:
                fig = px.bar(
                    signals_df, 
                    x="TRANSACTION_ID" if "TRANSACTION_ID" in signals_df.columns else list(signals_df.columns), 
                    y="AMOUNT" if "AMOUNT" in signals_df.columns else list(signals_df.columns), 
                    color="RISK_SCORE" if "RISK_SCORE" in signals_df.columns else None,
                    title="Anomalous Transaction Exposure & Associated Risk Index",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as chart_err:
                st.warning(f"📊 Visualization Layout Notice: {chart_err}")

            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            evidence = engine.gather_evidence(signals_df)
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            report_markdown = engine.generate_audit_report(signals_df, evidence)
            st.markdown(report_markdown)
            
            with st.spinner("Packaging binary PDF report layout..."):
                try:
                    import io
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib import colors
                    
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
                    
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], textColor=colors.HexColor('#8B0000'), fontSize=18, spaceAfter=12)
                    h2_style = ParagraphStyle('DocH2', parent=styles['Heading2'], textColor=colors.HexColor('#2F4F4F'), fontSize=12, spaceBefore=10, spaceAfter=6)
                    body_style = ParagraphStyle('DocBody', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=8)
                    table_text_style = ParagraphStyle('TableText', parent=styles['Normal'], fontSize=8, leading=10)
                    
                    story = []
                    story.append(Paragraph("SUSPICIOUS TRANSACTION REPORT (STR)", title_style))
                    story.append(Paragraph("<b>Generated By:</b> Risk-Gemma4-Agent System Cluster", body_style))
                    story.append(Paragraph("<b>Review Status:</b> PENDING HUMAN SIGN-OFF (Fail-Safe Local Mode)", body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📌 1. EXECUTIVE SUMMARY", h2_style))
                    summary_text = f"This official audit report summarizes a aggregation of suspicious network activities, encompassing <b>{total_incidents} flagged incidents</b> with a total capital exposure of <b>INR {total_flagged_amt:,}</b>."
                    story.append(Paragraph(summary_text, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("🔎 2. REGULATORY EVIDENCE RECOVERY FRAMEWORK", h2_style))
                    evidence_cleaned = evidence.replace("\n", "<br/>")
                    story.append(Paragraph(evidence_cleaned, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📊 3. ANALYTICAL AUDIT TRAIL PROFILE", h2_style))
                    table_data = [["TX ID", "ACC ID", "CUSTOMER NAME", "AMOUNT (INR)", "DEST", "RISK %", "KYC", "PEP"]]
                    
                    for idx, row in signals_df.head(25).iterrows():
                        table_data.append([
                            Paragraph(str(row.get("TRANSACTION_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("ACCOUNT_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("CUSTOMER_NAME", "N/A"))[:18], table_text_style),
                            Paragraph(f"₹{int(row.get('AMOUNT', 0)):,}", table_text_style),
                            Paragraph(str(row.get("COUNTRY_CODE", "N/A")), table_text_style),
                            Paragraph(f"{float(row.get('RISK_SCORE', 0)):.1f}%", table_text_style),
                            Paragraph(str(row.get("KYC_STATUS", "N/A")), table_text_style),
                            Paragraph("YES" if str(row.get("IS_PEP", "")).strip().upper() in ["TRUE", "YES"] else "NO", table_text_style)
                        ])
                    
                    # FIXED: Full 8-column layout dimensions explicitly defined to fix the syntax crash
                    col_widths = [45, 50, 110, 85, 40, 50, 60, 40]
                    pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                    pdf_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2F4F4F')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DCDCDC')),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ]))
                    story.append(pdf_table)
                    
                    doc.build(story)
                    pdf_data = pdf_buffer.getvalue()
                    
                    st.markdown("---")
                    st.success("✅ Professional Audit-Ready PDF compiled successfully!")
                    st.download_button(label="📥 Download Audit-Ready PDF Report", data=pdf_data, file_name="Gemma4_Suspicious_Transaction_Report.pdf", mime="application/pdf", use_container_width=True)
                except Exception as pdf_err:
                    st.error(f"❌ PDF Assembly Framework Notice: {pdf_err}")
# ==========================================
# ─── APP BLOCK 2: CONVERSATIONAL CHAT (TAB 2), LOOKUP (TAB 3) & REMEDIATION (TAB 4) ───
# ==========================================
with tab2:
    st.header("💬 Conversational CoCo Copilot")
    st.caption("Query real-time network liabilities and trace policy intersections interactively using Gemma 4.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask CoCo about current ledger anomalies..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("CoCo is tracing policy vectors via Gemma 4..."):
                try:
                    reference_df = engine.detect_signals(min_amount=min_threshold)
                    reference_df.columns = reference_df.columns.str.strip().str.upper()
                    policy_context = engine.gather_evidence(reference_df)
                    
                    # Core template structured cleanly using pure Python f-strings
                    chat_template = f"""
                    You are 'CoCo', an elite conversational AI Compliance Copilot powered by Gemma 4.
                    
                    ACTIVE DATA MATRIX LOG METRICS:
                    {reference_df[['TRANSACTION_ID', 'ACCOUNT_ID', 'AMOUNT', 'RISK_SCORE', 'IS_PEP']].head(15).to_string(index=False)}
                    
                    REGULATORY RULE CONTEXT snippets:
                    {policy_context}
                    
                    User Analytical Query: {user_prompt}
                    """
                    
                    from google.genai import types
                    response = engine.client.models.generate_content(
                        model='gemma-4-26b-a4b-it',
                        contents=chat_template,
                        config=types.GenerateContentConfig(
                            system_instruction="You are a professional corporate AML audit helper.",
                            temperature=0.1,
                            thinking_config=types.ThinkingConfig(thinking_level="low"),
                            max_output_tokens=2000
                        )
                    )
                    assistant_response = response.text
                    st.markdown(assistant_response)
                except Exception as chat_err:
                    assistant_response = f"❌ Inference Exception: {str(chat_err)}"
                    st.error(assistant_response)
                    
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

with tab3:
    st.header("📁 Corporate Account Directory Lookup")
    search_query = st.text_input("🔍 Search Account Master by ID or Entity Name:", placeholder="e.g., ACC_991")
    if search_query:
        filtered_master = engine.acc_df[engine.acc_df["ACCOUNT_ID"].astype(str).str.contains(search_query, case=False) | engine.acc_df["CUSTOMER_NAME"].astype(str).str.contains(search_query, case=False)]
        st.dataframe(filtered_master, use_container_width=True)

with tab4:
    st.header("🛠️ Operational Remediation & Actions Console")
    remediation_acc_list = engine.acc_df["ACCOUNT_ID"].unique()
    target_account = st.selectbox("Target Account ID for Interventions:", remediation_acc_list)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚨 Execute Temporary Debit Hold (60 Days)", type="secondary", use_container_width=True):
            st.warning(f"🔒 **System Override:** Debit hold mapped to **{target_account}** placed safely.")
    with c2:
        if st.button("📤 Export & File STR to FIU-IND Portal", type="primary", use_container_width=True):
            st.success(f"📤 **Regulatory Action Complete:** STR payload package routed to FIU-IND gateways.")
            
    st.markdown("---")
    auto_lock_pep = st.toggle("Auto-Lock unverified PEP cross-border paths instantly", value=True)
    restrict_velocity = st.toggle("Flag rapid velocity smurfing across 12-hour windows", value=False)
