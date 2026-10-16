# =====================================================================
# ─── RISK-GEMMA4-AGENT: OPERATIONAL MONITORING PANEL (TAB 1) ─────────
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
# ─── PART 2: EVIDENCE RAG GATHERING & POSITION-SAFE INFRASTRUCTURE ───
# =====================================================================
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            evidence = engine.gather_evidence(signals_df)
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            
            # Fetch active configuration thinking state matrix
            active_tier_token = st.session_state.get("active_thinking_level", "MINIMAL")
            
            # 🚨 FIX: Pass argument safely as a direct positional token parameter to ensure it matches the engine blueprint footprint perfectly
            report_markdown = engine.generate_audit_report(signals_df, evidence, active_tier_token)
            
            # 🛡️ THE PRESENTATION LAYER MANAGES STATE ASSEMBLY AND RENDERING HERE
            current_signoff = st.session_state.get('report_review_status', '⚠️ PENDING HUMAN SIGN-OFF')
            
            # Append the dynamic tracking operational signature footer cleanly
            final_rendered_view = (
                f"{report_markdown}\n\n"
                "---\n"
                "**Prepared By:** Risk-Gemma4-Agent System Cluster  \n"
                f"**Review Status:** {current_signoff}"
            )
            
            # Render out to target screen canvas components
            st.markdown(final_rendered_view)
