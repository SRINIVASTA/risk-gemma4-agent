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
        
        if not rem_log.empty:
            acc_actions = rem_log[(rem_log["ACCOUNT_ID"] == selected_acc_id) & (rem_log["STATUS"].isin(["ACTIVE_ENFORCED", "AUTO_ENFORCED"]))]
            if not acc_actions.empty: active_containment = acc_actions.iloc[-1]["ENFORCED_PROTOCOL"]

        risk_tier = "CRITICAL" if active_containment == "ACTIVE_LOCK" else "HIGH" if acc_record.get("IS_PEP") == True else "LOW"
            
        st.markdown("### Key Status")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric("KYC Status", f"✅ {acc_record.get('KYC_STATUS', 'N/A')}")
        kpi_col2.metric("Remediation", f"🚨 {active_containment}")
        kpi_col3.metric("PEP", f"⚠️ {'YES' if acc_record.get('IS_PEP') else 'NO'}")
        kpi_col4.metric("Risk Tier", f"🔴 {risk_tier}")
        
        st.markdown("---")
        st.subheader("Account Master Record")
        rec_col1, rec_col2 = st.columns(2)
        with rec_col1:
            st.markdown(f"**Account ID:** `{selected_acc_id}`")
            st.markdown(f"**Customer Name:** {acc_record.get('CUSTOMER_NAME', 'N/A')}")
            st.markdown(f"**Customer Type:** {acc_record.get('CUSTOMER_TYPE', 'N/A')}")
            if acc_record.get("CUSTOMER_TYPE") == "Corporate":
                st.markdown("**IEC Code:** `IEC_2401010101`")
                st.markdown("**Trade License:** `STAR_EXPORT_HOUSE`")
                st.markdown("**Primary Trade Role:** `BOTH`")
        with rec_col2:
            st.markdown(f"**Authorized AD Bank:** State Bank of India")
            st.markdown(f"**Current Balance:** ₹45,750,000" if selected_acc_id == "ACC_101" else f"**Current Balance:** ₹1,250,000")
            st.markdown("**GSTIN:** `27AABCS1429B1ZS`" if acc_record.get("CUSTOMER_TYPE") == "Corporate" else "**GSTIN:** `N/A`")
            st.markdown(f"**Tax Identifier (PAN):** `PAN-AABCS1429B`")
            st.markdown(f"**Permanent Address:** 14, Nariman Point, Cuffe Parade, Mumbai")

        st.markdown("---")
        st.subheader("Transaction History")
        if active_containment == "ACTIVE_LOCK":
            st.error("🔒 Account is ACTIVE_LOCK - Transaction ledger access blocked during investigation.")
        else:
            tx_subset = engine.tx_df[engine.tx_df["ACCOUNT_ID"] == selected_acc_id]
            st.dataframe(tx_subset, use_container_width=True)
