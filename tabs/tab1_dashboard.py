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
            
            # Normalize column names to uppercase text parameters safely
            signals_df.columns = signals_df.columns.str.strip().str.upper()
            
            # 🔗 SNOWFLAKE CORE HEADER MAPPING INTERLOCKS
            # Maps Snowflake schema columns down to base metrics tracking variables safely
            risk_col = "RISK_SCORE" if "RISK_SCORE" in signals_df.columns else "AMOUNT"
            time_col = "UPDATED_AT" if "UPDATED_AT" in signals_df.columns else "TIMESTAMP"
            status_col = "SYSTEMIC_LOCK_STATUS" if "SYSTEMIC_LOCK_STATUS" in signals_df.columns else "KYC_STATUS"
            
            total_flagged_amt = int(pd.to_numeric(signals_df["AMOUNT"], errors='coerce').fillna(0).sum())
            avg_risk_score = float(pd.to_numeric(signals_df[risk_col], errors='coerce').fillna(81.0).mean())
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🚨 Flagged Incidents Count", f"{total_incidents} Signals")
            col2.metric("💰 Total Capital Exposure", f"₹{total_flagged_amt:,}")
            col3.metric("⚠️ Average Network Risk Factor", f"{avg_risk_score:.1f}%")
            
            st.dataframe(signals_df, use_container_width=True)
            
            try:
                # Plots the interactive bar chart metrics dynamically without generating label errors
                x_axis_target = "TRANSACTION_ID" if "TRANSACTION_ID" in signals_df.columns else "ACCOUNT_ID"
                fig = px.bar(
                    signals_df, 
                    x=x_axis_target if x_axis_target in signals_df.columns else list(signals_df.columns)[0], 
                    y="AMOUNT", 
                    color=risk_col if risk_col in signals_df.columns else None, 
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
            
            # LIVE PROTOCOL OVERRIDE: Fetch state directly from Tab 4 controls
            current_signoff = st.session_state.get('report_review_status', '⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER')
            
            # Formulate the definitive compliance tracking metadata block
            final_rendered_view = (
                f"{report_markdown}\n\n"
                "---\n"
                "### 💡 4. RECOMMENDED COMPLIANCE ACTIONS\n"
                "* 🛡️ **Emergency Containment Protocol:** Immediately execute a targeted temporary debit hold for all Section 9.4 flagged mule accounts, limiting the hold to a strict maximum of **60 days**.\n"
                "* ⏳ **Time-Bound Resolution Protocol:** Initiate the time-bound resolution protocol: grant identified account holders a **20-day notification window** to submit official justification documents.\n"
                "* 📤 **External Regulatory Pipeline:** Route an urgent STR package to FIU-IND via the National Cyber Crime Reporting Portal (NCRP) interfaces within **30 days** for confirmed mule identities.\n"
                "* 🔒 **Ecosystem Interlock Enforcement:** Enforce the immediate global system lock on any pending PEP profiles executing cross-border transfers.\n\n"
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
                        val_risk_raw = row.get("RISK_SCORE", row.get(risk_col, 0))
                        try:
                            val_risk_pct = f"{float(val_risk_raw):.1f}%"
                        except ValueError:
                            val_risk_pct = f"{val_risk_raw}%" if pd.notna(val_risk_raw) else "81.0%"
                            
                        table_data.append([
                            Paragraph(str(row.get("TRANSACTION_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("ACCOUNT_ID", "N/A")), table_text_style),
                            Paragraph(str(row.get("CUSTOMER_NAME", "N/A"))[:18], table_text_style),
                            Paragraph(f"₹{int(pd.to_numeric(row.get('AMOUNT', 0), errors='coerce')):,}", table_text_style),
                            Paragraph(str(row.get("COUNTRY_CODE", row.get("DESTINATION", "IN"))), table_text_style),
                            Paragraph(val_risk_pct, table_text_style),
                            Paragraph(str(row.get("KYC_STATUS", row.get(status_col, "N/A"))), table_text_style)
                        ])
                    
                    # 🔧 FIXED: Restored column structural layout width definitions matching layout vectors
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
                    story.append(Spacer(1, 15))
                    
                    # 📥 REGULATORY MANDATE ATTACHMENTS FOR REPORTLAB CANVAS FLOWABLE STORY
                    story.append(Paragraph("💡 4. RECOMMENDED COMPLIANCE ACTIONS", h2_style))
                    story.append(Paragraph("• <b>🛡️ Emergency Containment Protocol:</b> Immediately execute a targeted temporary debit hold for all Section 9.4 flagged mule accounts, limiting the hold to a strict maximum of 60 days.", body_style))
                    story.append(Paragraph("• <b>⏳ Time-Bound Resolution Protocol:</b> Initiate the time-bound resolution protocol: grant identified account holders a 20-day notification window to submit official justification documents.", body_style))
                    story.append(Paragraph("• <b>📤 External Regulatory Pipeline:</b> Route an urgent STR package to FIU-IND via the National Cyber Crime Reporting Portal (NCRP) interfaces within 30 days for confirmed mule identities.", body_style))
                    story.append(Paragraph("• <b>🔒 Ecosystem Interlock Enforcement:</b> Enforce the immediate global system lock on any pending PEP profiles executing cross-border transfers.", body_style))
                    
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
