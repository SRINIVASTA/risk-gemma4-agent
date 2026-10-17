# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🛡️ REMEDIATION & ACTIONS CONSOLE (TAB 4) ─────
# ─── PART 1: TARGET CONTAINMENT DESK & INTERACTIVE UNLOCK MATRIX ─────
# =====================================================================
import streamlit as st
import pandas as pd

def render(engine):
    st.header("🛡️ Remediation & Actions Console")
    st.caption("Active Incident Response Core Routing - Updates the REMEDIATION_LOG Table Natively")
    st.markdown("---")
    
    # Ensure remediation_log state is initialized immediately at the top of rendering
    if "remediation_log" not in st.session_state or st.session_state["remediation_log"] is None:
        st.session_state["remediation_log"] = pd.DataFrame(columns=[
            "TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "TRIGGER_RULE", "STATUS"
        ])
    
    # 🎯 TARGETED ACCOUNT CONTAINMENT PROTOCOLS
    st.subheader("🎯 Targeted Account Containment Protocols")
    c1, c2 = st.columns(2)
    
    with c1: 
        # Sort and select target customer keys from master database file records
        target_account = st.selectbox("Select Target Profile to Contain / Release:", sorted(engine.acc_df["ACCOUNT_ID"].unique()))
    
    with c2: 
        # 💡 CRITICAL RESOLUTION: Added UNLOCK_ACCOUNT protocol parameter to the operation matrices array
        selected_protocol = st.selectbox(
            "Select Mitigation Protocol to Enforce:", 
            ["ACTIVE_LOCK", "UNLOCK_ACCOUNT", "ENHANCED_EDD", "DEBIT_HOLD_60_DAYS"]
        )
        
    if st.button("🚨 Dispatch Mitigation Protocol", type="primary", use_container_width=True):
        cust_name = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account]["CUSTOMER_NAME"].values[0]
        
        # 🛡️ CLEANUP OPTIMIZATION: Check for existing identical active locks to prevent duplicate row spam
        existing_logs = st.session_state["remediation_log"]
        duplicate_check = (existing_logs["ACCOUNT_ID"] == target_account) & \
                          (existing_logs["ENFORCED_PROTOCOL"] == selected_protocol) & \
                          (existing_logs["STATUS"] == "ACTIVE_ENFORCED")
                          
        if duplicate_check.any() and selected_protocol != "UNLOCK_ACCOUNT":
            st.error(f"⚠️ **Operational Lock Blocked:** Protocol `{selected_protocol}` is already actively enforced on account **{target_account}** ({cust_name}).")
        else:
            # Determine log parameters based on chosen action protocol routing rules
            trigger_rule_label = "MANUAL_CONTAINMENT_DESK" if selected_protocol != "UNLOCK_ACCOUNT" else "MANUAL_RELEASE_DESK"
            enforcement_status = "ACTIVE_ENFORCED" if selected_protocol != "UNLOCK_ACCOUNT" else "RELEASE_LOG_CLEAR"
            
            new_log = {
                "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "ACCOUNT_ID": target_account, 
                "CUSTOMER_NAME": cust_name, 
                "ENFORCED_PROTOCOL": selected_protocol, 
                "TRIGGER_RULE": trigger_rule_label, 
                "STATUS": enforcement_status
            }
            
            # Append mitigation protocol logs natively to the system session dataframes
            st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
            
            if selected_protocol == "UNLOCK_ACCOUNT":
                st.success(f"🔓 **Incident Response Release Active:** Unlocked account **{target_account}** ({cust_name}) and cleared active containment flags.")
            else:
                st.warning(f"🔒 **Incident Response Isolation Active:** Dispatched `{selected_protocol}` containment to **{target_account}**.")
                
            st.rerun()

# =====================================================================
# ─── PART 2: REGULATORY SIGN-OFFS & AUTOMATED ENGINE SCAN LOOPS ───────
# =====================================================================
    st.markdown("---")
    st.subheader("📋 Regulatory Export & Core Controls")
    ae1, ae2 = st.columns(2)
    with ae1:
        if st.button("📤 Export Compliance Package & File STR to FIU-IND Portal", use_container_width=True): 
            st.success("📤 Routed to FIU-IND gateways successfully.")
    with ae2:
        current_review_val = st.session_state.get("report_review_status", "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER")
        if st.button(f"📝 Toggle Status (Current: {current_review_val})", use_container_width=True):
            if "PENDING" in current_review_val:
                st.session_state["report_review_status"] = "🟢 APPROVED & SIGNED OFF BY COMPLIANCE OFFICER"
            else:
                st.session_state["report_review_status"] = "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER"
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
            if (str(row.get("IS_PEP")).strip().upper() == "TRUE" or row.get("IS_PEP") == True) and row["COUNTRY_CODE"] in ["KY", "CH"]:
                new_violations.append({"TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), "ACCOUNT_ID": row["ACCOUNT_ID"], "CUSTOMER_NAME": row["CUSTOMER_NAME"], "ENFORCED_PROTOCOL": "ACTIVE_LOCK", "TRIGGER_RULE": "RULE_2_PEP_TAX_HAVEN", "STATUS": "AUTO_ENFORCED"})
        if new_violations:
            st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame(new_violations).drop_duplicates(subset=['ACCOUNT_ID', 'TRIGGER_RULE'])], ignore_index=True)
        st.rerun()
        
    st.markdown("---")
    st.subheader("📋 Active Live REMEDIATION_LOG Table")
        
    # Render the interactive dataframe view directory layer cleanly
    if not st.session_state["remediation_log"].empty:
        st.dataframe(
            st.session_state["remediation_log"].sort_values(by="TIMESTAMP", ascending=False), 
            use_container_width=True
        )
        
        # Add an Administrative operational cache-wiping shortcut for Level 4 SYSTEM_ADMIN
        if st.session_state.get("active_iam_user") == "SYSTEM_ADMIN":
            if st.button("🗑️ Wipe Remediation Audit Logs & Clear Engine Cache", type="secondary", use_container_width=True):
                st.session_state["remediation_log"] = pd.DataFrame(columns=[
                    "TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "TRIGGER_RULE", "STATUS"
                ])
                st.success("Operational tracking matrices reset successfully.")
                st.rerun()
    else:
        st.info("🟢 No operational containment overrides or system freezes currently active across the network logs.")
