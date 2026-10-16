# =====================================================================
# ─── RISK-GEMMA4-AGENT: OPERATIONAL MONITORING PANEL (TAB 1) ─────────
# ─── PART 1: SIGNAL EXPOSURE DETECTION & VISUALISATION GRAPHICS ──────
# =====================================================================
import streamlit as st
import plotly.express as px
import pandas as pd

def render(engine, min_threshold):
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
            col1.metric("🚨 Flagged Incidents Count", f"{total_incidents} Signals")
            col2.metric("💰 Total Capital Exposure", f"₹{total_flagged_amt:,}")
            col3.metric("⚠️ Average Network Risk Factor", f"{avg_risk_score:.1f}%")
            
            st.dataframe(signals_df, use_container_width=True)
            
            try:
                fig = px.bar(
                    signals_df, 
                    x="TRANSACTION_ID" if "TRANSACTION_ID" in signals_df.columns else list(signals_df.columns), 
                    y="AMOUNT", 
                    color="RISK_SCORE", 
                    title="Anomalous Transaction Exposure", 
                    color_continuous_scale="Reds"
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as chart_err: 
                st.warning(f"📊 Visualization Layout Notice: {chart_err}")
# =====================================================================
# ─── PART 2: EVIDENCE RAG GATHERING & REPORTLAB BINARY PDF BUILDER ───
# =====================================================================
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            evidence = engine.gather_evidence(signals_df)
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            
            # Fetch active configuration thinking tier token string directly
            active_tier_token = st.session_state.get("active_thinking_level", "MINIMAL")
            report_markdown = engine.generate_audit_report(signals_df, evidence, active_tier_token)
            
            # 🚨 LIVE PROTOCOL OVERRIDE: Fetch state directly from Tab 4 controls
            current_signoff = st.session_state.get('report_review_status', '⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER')
            
            # Formulate the definitive compliance tracking metadata block
            final_rendered_view = (
                f"{report_markdown}\n\n"
                "---\n"
                "**Prepared By:** Risk-Gemma4-Agent System Cluster  \n"
                f"**Review Status:** {current_signoff}"
            )
            
            # Print to screen container layout
            st.markdown(final_rendered_view)
            
            # ─── 📥 REPORTLAB PDF ASSEMBLY LAYOUT ───
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
                    story.append(Paragraph(f"<b>Review Status:</b> {current_signoff}", body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📌 1. EXECUTIVE SUMMARY", h2_style))
                    summary_text = f"This official audit report summarizes an aggregation of suspicious network activities, encompassing <b>{total_incidents} flagged incidents</b> with a total capital exposure of <b>INR {total_flagged_amt:,}</b>. Inherent network threat profiling indicates average vulnerabilities standing at <b>{avg_risk_score:.1f}%</b>."
                    story.append(Paragraph(summary_text, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("🔎 2. REGULATORY EVIDENCE RECOVERY FRAMEWORK", h2_style))
                    evidence_cleaned = evidence.replace("\n", "<br/>")
                    story.append(Paragraph(evidence_cleaned, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📊 3. ANALYTICAL AUDIT TRAIL PROFILE", h2_style))
                    table_data = [["TX ID", "ACC ID", "CUSTOMER NAME", "AMOUNT (INR)", "DEST", "RISK %", "KYC"]]
                    
                    # Core loop extraction to inject rows safely into the PDF table grid matrix
                    for idx, row in signals_df.head(30).iterrows():
                        table_data.append([
                            Paragraph(str(row.get("TRANSACTION_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("ACCOUNT_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("CUSTOMER_NAME", "N/A"))[:18], table_text_style),
                            Paragraph(f"₹{int(row.get('AMOUNT', 0)):,}", table_text_style),
                            Paragraph(str(row.get("COUNTRY_CODE", "N/A")), table_text_style),
                            Paragraph(f"{float(row.get('RISK_SCORE', 0)):.1f}%", table_text_style),
                            Paragraph(str(row.get("KYC_STATUS", "N/A")), table_text_style)
                        ])
                    
                    col_widths = [50, 55, 130, 90, 45, 55, 55]
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
                    st.download_button(
                        label="📥 Download Audit-Ready PDF Report", 
                        data=pdf_data, 
                        file_name="Gemma4_Suspicious_Transaction_Report.pdf", 
                        mime="application/pdf", 
                        use_container_width=True
                    )
                except Exception as pdf_err:
                    st.error(f"❌ PDF Assembly Framework Notice: {pdf_err}")
