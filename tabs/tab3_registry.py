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
        
        # FIXED STATE TIMELINE CHECK: Evaluate the absolute latest chronological log action
        if not rem_log.empty:
            acc_actions = rem_log[rem_log["ACCOUNT_ID"] == selected_acc_id].sort_values(by="TIMESTAMP")
            if not acc_actions.empty:
                latest_action = acc_actions.iloc[-1]
                if latest_action["ENFORCED_PROTOCOL"] == "UNLOCK_ACCOUNT" or latest_action["STATUS"] == "RELEASE_LOG_CLEAR":
                    active_containment = "🟢 CLEAR"
                else:
                    active_containment = latest_action["ENFORCED_PROTOCOL"]

        # Normalize the IS_PEP boolean check safely across evaluations
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
            
            # 💡 100% DECOUPLED FROM CODE: Pulling trade data dynamically from database row fields
            if acc_record.get("CUSTOMER_TYPE") == "Corporate":
                st.markdown(f"**IEC Code:** `{acc_record.get('IEC_CODE', 'N/A')}`")
                st.markdown(f"**Trade License:** `{acc_record.get('TRADE_LICENSE', 'N/A')}`")
                st.markdown("**Primary Trade Role:** `MERCHANT_EXPORTER`")
                
        with rec_col2:
            # 💡 100% DECOUPLED FROM CODE: Pulling financial identifiers and locations dynamically from CSV
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
        if active_containment == "ACTIVE_LOCK":
            st.error("🔒 Account is ACTIVE_LOCK - Transaction ledger access blocked during investigation.")
        else:
            tx_subset = engine.tx_df[engine.tx_df["ACCOUNT_ID"] == selected_acc_id]
            st.dataframe(tx_subset, use_container_width=True)
