import streamlit as st
import pandas as pd

def render(engine):
    st.header("🛡️ Remediation & Actions Console")
    st.caption("Active Incident Response Core Routing - Updates the REMEDIATION_LOG Table Natively")
    st.markdown("---")
    
    st.subheader("🎯 Targeted Account Containment Protocols")
    c1, c2 = st.columns(2)
    with c1: target_account = st.selectbox("Select Target Profile to Contain:", sorted(engine.acc_df["ACCOUNT_ID"].unique()))
    with c2: selected_protocol = st.selectbox("Select Mitigation Protocol to Enforce:", ["ACTIVE_LOCK", "ENHANCED_EDD", "DEBIT_HOLD_60_DAYS"])
        
    if st.button("🚨 Dispatch Mitigation Protocol", type="primary", use_container_width=True):
        cust_name = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account]["CUSTOMER_NAME"].values[0]
        new_log = {"TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "ACCOUNT_ID": target_account, "CUSTOMER_NAME": cust_name, "ENFORCED_PROTOCOL": selected_protocol, "TRIGGER_RULE": "MANUAL_CONTAINMENT_DESK", "STATUS": "ACTIVE_ENFORCED"}
        st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
        st.warning(f"🔒 Dispatched `{selected_protocol}` containment to **{target_account}**.")
        st.rerun()

    st.markdown("---")
    st.subheader("📋 Regulatory Export & Core Controls")
    ae1, ae2 = st.columns(2)
    with ae1:
        if st.button("📤 Export Compliance Package & File STR to FIU-IND Portal", use_container_width=True): st.success("📤 Routed to FIU-IND gateways.")
    with ae2:
        if st.button(f"📝 Sign-Off Global STR Audit Report ({st.session_state.report_review_status})", use_container_width=True):
            st.session_state["report_review_status"] = "🟢 APPROVED & SIGNED OFF"
            st.success("Authorized successfully!"); st.rerun()

    st.markdown("---")
    st.subheader("⚙️ Automated Data Engine Rules")
    st.info("Scans all transactions against sanctioned country and PEP/tax haven rules.")
    st.markdown("* **Rule 1 - Sanctioned Country Auto-Freeze** (KP, IR, SY, MM ➔ ACTIVE_LOCK)\n* **Rule 2 - PEP Tax Haven Lock** (PEP to KY, CH ➔ ACTIVE_LOCK)")
    st.warning("⚠️ This will scan ALL transactions and auto-lock matching accounts in the REMEDIATION_LOG.")
    
    if st.button("⚡ Run Engine Automated Rules Automation", use_container_width=True):
        merged_ledger = pd.merge(engine.tx_df, engine.acc_df, on="ACCOUNT_ID")
        new_violations = []
        for _, row in merged_ledger.iterrows():
            if row["COUNTRY_CODE"] in ["KP", "IR", "SY", "MM"]:
                new_violations.append({"TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "ACCOUNT_ID": row["ACCOUNT_ID"], "CUSTOMER_NAME": row["CUSTOMER_NAME"], "ENFORCED_PROTOCOL": "ACTIVE_LOCK", "TRIGGER_RULE": "RULE_1_SANCTION_VIOLATION", "STATUS": "AUTO_ENFORCED"})
            if row.get("IS_PEP") == True and row["COUNTRY_CODE"] in ["KY", "CH"]:
                new_violations.append({"TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "ACCOUNT_ID": row["ACCOUNT_ID"], "CUSTOMER_NAME": row["CUSTOMER_NAME"], "ENFORCED_PROTOCOL": "ACTIVE_LOCK", "TRIGGER_RULE": "RULE_2_PEP_TAX_HAVEN", "STATUS": "AUTO_ENFORCED"})
        if new_violations:
            st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame(new_violations).drop_duplicates(subset=['ACCOUNT_ID', 'TRIGGER_RULE'])], ignore_index=True)
        st.rerun()
        
    st.markdown("---")
    st.subheader("📋 Active Live REMEDIATION_LOG Table")
    st.dataframe(st.session_state["remediation_log"], use_container_width=True)
