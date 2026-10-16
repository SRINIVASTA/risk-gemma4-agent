# =====================================================================
# ─── RISK-GEMMA4-AGENT: OPERATIONAL MONITIORING PANEL (TAB 1) ────────
# ─── PART 1: SIGNAL EXPOSURE DETECTION & VISUALISATION GRAPHICS ──────
# =====================================================================
import streamlit as st
import plotly.express as px

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
# ─── PART 2: EVIDENCE RAG GATHERING & DYNAMIC STATE FOOTER RENDERING ─
# =====================================================================
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            evidence = engine.gather_evidence(signals_df)
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            
            # Pass the explicit active thinking tier token string directly to the model pipeline
            active_tier_token = st.session_state.get("active_thinking_level", "MINIMAL")
            report_markdown = engine.generate_audit_report(signals_df, evidence, active_thinking_level=active_tier_token)
            
            # 🚨 LIVE PROTOCOL FIX: Pull the active status dynamically driven by Tab 4 right now!
            current_signoff = st.session_state.get('report_review_status', '⚠️ PENDING HUMAN SIGN-OFF')
            
            # Combine the two elements seamlessly in presentation memory
            final_rendered_view = (
                f"{report_markdown}\n\n"
                "---\n"
                "**Prepared By:** Risk-Gemma4-Agent System Cluster  \n"
                f"**Review Status:** {current_signoff}"
            )
            
            # Print the final report to the workspace container layout
            st.markdown(final_rendered_view)
