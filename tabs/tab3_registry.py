# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🔍 CUSTOMER 360 PROFILE REGISTRY (TAB 3) ─────
# ─── PART 1: ACCOUNT MASTER LOOKUP & TIMELINE INTERLOCK MATRICES ─────
# =====================================================================
import streamlit as st
import pandas as pd

def render(engine):
    st.header("🔍 Customer 360 Account Profile Registry")
    st.caption("Select any customer to view full account master details, remediation status, and transaction history.")
    st.markdown("---")
    
    account_list = sorted(engine.acc_df["ACCOUNT_ID"].unique())
    selected_acc_id = st.selectbox("Select Account ID:", account_list, key="customer_360_selector")
    
    if selected_acc_id:
        acc_record = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == selected_acc_id].iloc[0]
        rem_log = st.session_state.get("remediation_log", pd.DataFrame())
        active_containment = "🟢 CLEAR"
        
        # 🔗 SNOWFLAKE COMPATIBILITY INTERLOCK: Evaluate chronological actions via structural updates
        if not rem_log.empty:
            acc_actions = rem_log[rem_log["ACCOUNT_ID"] == selected_acc_id]
            
            if not acc_actions.empty:
                # Determine correct time-tracking column naming rules present on the layout
                time_col = "UPDATED_AT" if "UPDATED_AT" in acc_actions.columns else "TIMESTAMP"
                status_col = "SYSTEMIC_LOCK_STATUS" if "SYSTEMIC_LOCK_STATUS" in acc_actions.columns else "ENFORCED_PROTOCOL"
                clearance_col = "KYC_STEP_UP_LEVEL" if "KYC_STEP_UP_LEVEL" in acc_actions.columns else "STATUS"
                
                # Sort sequentially to find the absolute latest operational parameter state
                acc_actions = acc_actions.sort_values(by=time_col)
                latest_action = acc_actions.iloc[-1]
                
                # Dynamic translation logic catching both local and Snowflake protocol values
                if latest_action[status_col] in ["UNLOCK_ACCOUNT", "UNLOCKED"] or latest_action[clearance_col] in ["RELEASE_LOG_CLEAR", "UNLOCKED"]:
                    active_containment = "🟢 CLEAR"
                else:
                    active_containment = latest_action[status_col]

        # Normalize the IS_PEP boolean check safely across text structures
        is_pep_active = str(acc_record.get("IS_PEP")).strip().upper() == "TRUE" or acc_record.get("IS_PEP") == True
        risk_tier = "CRITICAL" if active_containment == "ACTIVE_LOCK" else "HIGH" if is_pep_active else "LOW"
            
        st.markdown("### Key Status")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric("KYC Status", f"✅ {acc_record.get('KYC_STATUS', 'N/A')}")
        
        if active_containment == "🟢 CLEAR":
            kpi_col2.metric("Remediation", active_containment)
        else:
            kpi_col2.metric("Remediation", f"🚨 {active_containment}")
            
        kpi_col3.metric("PEP", f"⚠️ {'YES' if is_pep_active else 'NO'}")
        kpi_col4.metric("Risk Tier", f"🔴 {risk_tier}")
        st.markdown("---")
        st.subheader("Account Master Record")
        rec_col1, rec_col2 = st.columns(2)
        with rec_col1:
            st.markdown(f"**Account ID:** `{selected_acc_id}`")
            st.markdown(f"**Customer Name:** {acc_record.get('CUSTOMER_NAME', 'N/A')}")
            st.markdown(f"**Customer Type:** {acc_record.get('CUSTOMER_TYPE', 'N/A')}")
            
            # Pulling trade data dynamically from database row fields
            if acc_record.get("CUSTOMER_TYPE") == "Corporate":
                st.markdown(f"**IEC Code:** `{acc_record.get('IEC_CODE', 'N/A')}`")
                st.markdown(f"**Trade License:** `{acc_record.get('TRADE_LICENSE', 'N/A')}`")
                st.markdown("**Primary Trade Role:** `MERCHANT_EXPORTER`")
                
        with rec_col2:
            # Pulling financial identifiers and locations dynamically from active schema vectors
            st.markdown(f"**Authorized AD Bank:** {acc_record.get('AD_BANK', 'N/A')}")
            try:
                formatted_bal = f"₹{int(acc_record.get('CURRENT_BALANCE', 0)):,}"
            except ValueError:
                formatted_bal = f"₹{acc_record.get('CURRENT_BALANCE', 'N/A')}"
            st.markdown(f"**Current Balance:** {formatted_bal}")
            st.markdown(f"**GSTIN:** `{acc_record.get('GSTIN', 'N/A')}`")
            st.markdown(f"**Tax Identifier (PAN):** `{acc_record.get('PAN', 'N/A')}`")
            st.markdown(f"**Permanent Address:** {acc_record.get('PERMANENT_ADDRESS', 'N/A')}")

        st.markdown("---")
        st.subheader("Transaction History")
        
        # 🛡️ CRISIS CONTROL INTERLOCK: Blocks transactional lookups if system contains an active ACTIVE_LOCK state
        if active_containment == "ACTIVE_LOCK":
            st.error("🔒 Account is ACTIVE_LOCK - Transaction ledger access blocked during investigation.")
        else:
            clean_tx = engine.tx_df[engine.tx_df["TRANSACTION_ID"] != "TRANSACTION_ID"]
            tx_subset = clean_tx[clean_tx["ACCOUNT_ID"] == selected_acc_id]
            
            if not tx_subset.empty:
                st.dataframe(tx_subset.sort_values(by="TIMESTAMP", ascending=False), use_container_width=True)
            else:
                st.info("ℹ️ No transactions recorded for this client entity.")
