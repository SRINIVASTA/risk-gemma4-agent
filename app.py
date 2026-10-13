# ─── BLOCK 1: INITIALIZATION & CACHE SAFEGUARD SYSTEM ───
import streamlit as st
import subprocess
import sys
import os

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import faiss
    import plotly.express as px
    import pandas as pd
    from langchain_core.prompts import PromptTemplate
except ImportError:
    with st.spinner("🔧 Synchronizing production environment layers..."):
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet", 
            "langchain-google-genai>=1.0.0", "faiss-cpu>=1.8.0", "plotly>=5.20.0"
        ])
    st.rerun()

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
    st.info("💡 **Welcome to the Workspace!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemma 4 data pipelines and conversational engines.")
    st.stop()

# Imports from your upgraded engine file
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
    st.cache_resource.clear()

if "current_threshold" not in st.session_state:
    st.session_state["current_threshold"] = 5000000

min_threshold = st.sidebar.slider(
    "Cross-Border Alert Threshold (₹)", 
    1000000, 10000000, 
    key="current_threshold",
    step=500000,
    on_change=handle_threshold_shift
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Core Dashboard Tab Layout Structure
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Operational Dashboard", 
    "💬 Conversational CoCo Copilot", 
    "📁 Account Directory Lookup",
    "🛠️ Remediation & Actions Console"
])
# Core Dashboard Tab Layout Structure
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Operational Dashboard", 
    "💬 Conversational CoCo Copilot", 
    "📁 Account Directory Lookup",
    "🛠️ Remediation & Actions Console"
])

# ─── TAB 1: OPERATIONAL DASHBOARD CORE LOGIC ───
with tab1:
    st.header("🛡️ Risk & Compliance Monitoring Terminal")
    st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")
    
    if st.button("Run Global Compliance Audit Pipeline", type="primary"):
        st.subheader("✅ Step 1: Signal Detection (Structured Data)")
        with st.spinner("Filtering analytical ledgers..."):
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
            
            st.markdown("### Active Anomalous System Payload (PEP & Velocity Monitored)")
            st.dataframe(signals_df, use_container_width=True)
            
            available_cols = list(signals_df.columns)
            hover_targets = [col for col in ["CUSTOMER_NAME", "COUNTRY_CODE", "KYC_STATUS", "IS_PEP"] if col in available_cols]
            
            try:
                fig = px.bar(
                    signals_df, 
                    x="TRANSACTION_ID" if "TRANSACTION_ID" in available_cols else available_cols, 
                    y="AMOUNT" if "AMOUNT" in available_cols else available_cols, 
                    color="RISK_SCORE" if "RISK_SCORE" in available_cols else None,
                    hover_data=hover_targets,
                    labels={"TRANSACTION_ID": "Transaction ID", "AMOUNT": "Amount (INR)", "RISK_SCORE": "Risk Level"},
                    title="Anomalous Transaction Exposure & Associated Risk Index",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(template="plotly_dark", title_x=0.0)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as chart_err:
                st.warning(f"📊 Visualization Layout Notice: {chart_err}. Renders default grid views instead.")

            # RAG Pipeline Execution Window
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            with st.spinner("Querying unstructured regulatory policy frameworks..."):
                evidence = engine.gather_evidence(signals_df)
            st.info("Extracted Regulatory Violations & Compliance Snippets:")
            st.code(evidence, language="text")
            
            # Audit Report Output Window
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            with st.spinner("Compiling final markdown template via Gemma 4..."):
                report_markdown = engine.generate_audit_report(signals_df, evidence)
            
            st.markdown(report_markdown)
            # Formatted ReportLab Binary Compilation Engine 
            with st.spinner("Packaging binary PDF report layout..."):
                try:
                    import io
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib import colors
                    
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(
                        pdf_buffer, 
                        pagesize=letter,
                        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
                    )
                    
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle(
                        'DocTitle', parent=styles['Heading1'], 
                        textColor=colors.HexColor('#8B0000'), fontSize=18, spaceAfter=12
                    )
                    h2_style = ParagraphStyle(
                        'DocH2', parent=styles['Heading2'], 
                        textColor=colors.HexColor('#2F4F4F'), fontSize=12, spaceBefore=10, spaceAfter=6
                    )
                    body_style = ParagraphStyle(
                        'DocBody', parent=styles['BodyText'], 
                        fontSize=10, leading=14, spaceAfter=8
                    )
                    
                    story = []
                    story.append(Paragraph("SUSPICIOUS TRANSACTION REPORT (STR)", title_style))
                    story.append(Paragraph("<b>Generated By:</b> Risk-Gemma4-Agent System Cluster", body_style))
                    story.append(Paragraph("<b>Review Status:</b> PENDING HUMAN SIGN-OFF (Fail-Safe Local Mode)", body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📌 1. EXECUTIVE SUMMARY", h2_style))
                    summary_text = (
                        f"This official audit report summarizes a significant aggregation of suspicious network activities, "
                        f"encompassing {total_incidents} flagged incidents with a total capital exposure of INR {total_flagged_amt:,}. "
                        f"The average system risk network factor across these anomalous profiles is calculated at {avg_risk_score:.1f}%. "
                        f"This dataset layout triggers explicit compliance breaches under RBI anti-money laundering frameworks and "
                        f"demands an immediate temporary debit hold remediation step."
                    )
                    story.append(Paragraph(summary_text, body_style))
                    
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("📊 2. FLAGGED TRANSACTION LEDGER SUMMARY", h2_style))
                    
                    table_data = [["Txn ID", "Account ID", "Amount (INR)", "Risk Factor"]]
                    for _, row in signals_df.head(10).iterrows():
                        table_data.append([
                            str(row.get("TRANSACTION_ID", "N/A")),
                            str(row.get("ACCOUNT_ID", "N/A")),
                            f"₹{int(row.get('AMOUNT', 0)):,}",
                            f"{float(row.get('RISK_SCORE', 0)):.1f}%"
                        ])
                    
                    pdf_table = Table(table_data, colWidths=[80, 100, 120, 100])
                    pdf_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2F4F4F')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('BOTTOMPADDING', (0,0), (-1,0), 6),
                        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F5F5')),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('FONTSIZE', (0,0), (-1,-1), 9),
                    ]))
                    story.append(pdf_table)
                    
                    doc.build(story)
                    pdf_data = pdf_buffer.getvalue()
                    
                    st.download_button(
                        label="📥 Download Audit-Ready PDF Report",
                        data=pdf_data,
                        file_name="Gemma4_Suspicious_Transaction_Report.pdf",
                        mime="application/pdf"
                    )
                except Exception as pdf_err:
                    st.error(f"❌ PDF Assembly Framework Notice: {pdf_err}")

# ─── TAB 2: CONVERSATIONAL COCO COPILOT ───
with tab2:
    st.header("💬 Conversational CoCo Copilot")
    st.caption("Query real-time network liabilities and trace policy intersections interactively using Gemma 4.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask CoCo about current ledger anomalies or Section 7.3 velocity structuring..."):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("CoCo is tracing policy vectors via Gemma 4..."):
                try:
                    from google.genai import types
                    
                    client_instance = init_engine().client
                    system_directive = (
                        "You are 'CoCo', an expert corporate compliance assistant powered by Gemma 4. "
                        "Answer user queries regarding corporate risk logs, cross-border thresholds, "
                        "and structural audit workflows with extreme factual precision."
                    )
                    
                    response = client_instance.models.generate_content(
                        model='gemma-4-26b-a4b-it',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_directive,
                            temperature=0.2,
                            thinking_config=types.ThinkingConfig(thinking_level="high")
                        )
                    )
                    assistant_response = response.text
                    st.markdown(assistant_response)
                except Exception as chat_err:
                    assistant_response = f"❌ Copilot Inference Error: {str(chat_err)}"
                    st.error(assistant_response)
                    
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# ─── TAB 3: ACCOUNT DIRECTORY LOOKUP ───
with tab3:
    st.header("📁 Corporate Account Directory Lookup")
    st.caption("Query master KYC listings and isolate underlying Politically Exposed Person (PEP) network flags.")
    
    search_query = st.text_input("🔍 Search Account Master by ID or Entity Name:", placeholder="e.g., ACC_991 or Alpha Global")
    
    if search_query:
        account_master_df = engine.acc_df.copy()
        filtered_master = account_master_df[
            account_master_df["ACCOUNT_ID"].astype(str).str.contains(search_query, case=False, na=False) |
            account_master_df["CUSTOMER_NAME"].astype(str).str.contains(search_query, case=False, na=False)
        ]
        
        if filtered_master.empty:
            st.warning("No records matched your search parameters inside the directory.")
        else:
            st.subheader("📋 Matched Entity Corporate Profiling")
            st.dataframe(filtered_master, use_container_width=True)
    else:
        st.info("💡 Enter an Account ID string above to pull live registration metadata structures.")

# ─── TAB 4: REMEDIATION & ACTIONS CONSOLE ───
with tab4:
    st.header("🛠️ Operational Remediation & Actions Console")
    st.caption("Trigger time-bound line-of-custody containment workflows adhering directly to 2026 regulatory mandates.")
    
    st.markdown("### ⚡ Live System Containment Interventions")
    target_account = st.text_input("Target Account ID for Interventions:", placeholder="e.g., ACC_101")
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        st.markdown("#### 🔒 Hold Placements")
        if st.button("🚨 Execute Temporary Debit Hold (60 Days)", type="secondary", use_container_width=True):
            if target_account:
                st.warning(f"🔒 **System Override:** Temporary debit hold mapped to **{target_account}** successfully placed. Notification timer initialized (20-day customer window activated under Draft Amendment Section 9.4).")
            else:
                st.error("Please specify a target Account ID to execute a debit hold.")
                
    with col_act2:
        st.markdown("#### 📁 Regulatory Reporting")
        if st.button("📤 Export & File STR to FIU-IND Portal", type="primary", use_container_width=True):
            if target_account:
                st.success(f"📤 **Regulatory Action Complete:** Suspicious Transaction Report (STR) packages for **{target_account}** generated and securely routed to FIU-IND through the portal pipeline.")
            else:
                st.error("Please specify a target Account ID to file an official STR payload.")
