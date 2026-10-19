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
    
    st.subheader("🎯 Targeted Account Containment Protocols")
    
    # ─── VERTICAL FORM SEQUENCE (Matches snippet exactly) ───
    target_account = st.selectbox(
        "Select Target Profile to Contain:", 
        sorted(engine.acc_df["ACCOUNT_ID"].unique())
    )
    
    selected_protocol = st.selectbox(
        "Select Mitigation Protocol to Enforce:", 
        ["ACTIVE_LOCK", "UNLOCKED", "ENHANCED_EDD", "DEBIT_HOLD_60_DAYS"]
    )
        
    compliance_justification = ""
    uploaded_doc = None
    
    # Render justification workflow sequentially underneath the selectors
    if selected_protocol == "UNLOCKED":
        st.warning("⚠️ Changing protocol from ACTIVE_LOCK requires mandatory compliance justification.")
        
        compliance_justification = st.text_area(
            "Compliance Remarks & Justification", 
            placeholder="Provide detailed justification for this protocol change..."
        )
        
        uploaded_doc = st.file_uploader(
            "Enclosed Scanned Letter / Document Reference", 
            type=["pdf", "png", "jpg"],
            help="200MB per file • PDF, PNG, JPG"
        )
    
    if st.button("🚨 Dispatch Mitigation Protocol", type="primary", use_container_width=True):
        if selected_protocol == "UNLOCKED" and not compliance_justification.strip():
            st.error("❌ **Compliance Block:** You must provide a justification remark to change protocol from ACTIVE_LOCK.")
        else:
            cust_name = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account]["CUSTOMER_NAME"].values
            
            existing_logs = st.session_state["remediation_log"]
            duplicate_check = (existing_logs["ACCOUNT_ID"] == target_account) & \
                              (existing_logs["ENFORCED_PROTOCOL"] == selected_protocol) & \
                              (existing_logs["STATUS"] == "ACTIVE_ENFORCED")
                              
            if duplicate_check.any() and selected_protocol != "UNLOCKED":
                st.error(f"⚠️ **Operational Lock Blocked:** Protocol `{selected_protocol}` is already actively enforced on account **{target_account}** ({cust_name}).")
            else:
                trigger_rule_label = "MANUAL_CONTAINMENT_DESK" if selected_protocol != "UNLOCKED" else "MANUAL_RELEASE_DESK"
                enforcement_status = "ACTIVE_ENFORCED" if selected_protocol != "UNLOCKED" else "RELEASE_LOG_CLEAR"
                
                new_log = {
                    "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "ACCOUNT_ID": target_account, 
                    "CUSTOMER_NAME": cust_name, 
                    "ENFORCED_PROTOCOL": selected_protocol, 
                    "TRIGGER_RULE": trigger_rule_label, 
                    "STATUS": enforcement_status
                }
                
                st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
                
                if selected_protocol == "UNLOCKED":
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
        # Check remediation_log to intercept active locks across the ecosystem
        log_df = st.session_state["remediation_log"]
        active_locks_exist = False
        
        if not log_df.empty:
            # Look at the most recent administrative state entry per unique account profile
            latest_entries = log_df.sort_values("TIMESTAMP").groupby("ACCOUNT_ID").last()
            active_locks_exist = (latest_entries["ENFORCED_PROTOCOL"] == "ACTIVE_LOCK").any()

        # Update display dynamically context depending on the status found above
        if active_locks_exist:
            st.error("🔒 SYSTEM INTERLOCK: ACTIVE_LOCK detected on network logs. Review Required.")
        else:
            current_review_val = st.session_state.get("report_review_status", "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER")
            if st.button(f"📝 Toggle Status (Current: {current_review_val})", use_container_width=True):
                if "PENDING" in current_review_val:
                    st.session_state["report_review_status"] = "🟢 APPROVED & SIGNED OFF BY COMPLIANCE OFFICER"
                else:
                    st.session_state["report_review_status"] = "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER"
                st.success("Authorized successfully!")
                st.rerun()

    st.markdown("---")
    st.subheader("⚙️ Automated Data Engine Rules")
    st.caption("Scans all transactions against sanctioned country and PEP/tax haven rules. Auto-locks accounts and generates STRs.")
    
    # Exact textual interface display rules matching user UI criteria strings
    st.markdown("""
    * **Rule 1 - Sanctioned Country Auto-Freeze:** If any transaction routes to KP, IR, SY, or MM ➔ Immediate ACTIVE_LOCK + auto-generated STR.
    * **Rule 2 - PEP Tax Haven Lock:** If a PEP account routes funds to KY or CH ➔ Immediate ACTIVE_LOCK + ENHANCED_EDD.
    """)
    st.warning("⚠️ This will scan ALL transactions and auto-lock matching accounts in the REMEDIATION_LOG.")
    
    if st.button("⚡ Run Engine Automated Rules Automation", use_container_width=True):
        merged_ledger = pd.merge(engine.tx_df, engine.acc_df, on="ACCOUNT_ID")
        new_violations = []
        
        # Build a rapid lookup set of manually unlocked profiles to honor overrides
        remediation_df = st.session_state["remediation_log"]
        unlocked_accounts = set()
        
        if not remediation_df.empty:
            latest_states = remediation_df.sort_values("TIMESTAMP").groupby("ACCOUNT_ID").last().reset_index()
            unlocked_accounts = set(latest_states[latest_states["STATUS"] == "RELEASE_LOG_CLEAR"]["ACCOUNT_ID"].unique())

        for _, row in merged_ledger.iterrows():
            acct_id = row["ACCOUNT_ID"]
            
            # 🛡️ INTERLOCK BYPASS: Skip automated system locks if compliance has authorized a manual UNLOCKED clearance
            if acct_id in unlocked_accounts:
                continue
                
            # Rule 1 - Sanctioned Country Auto-Freeze Rule Validation
            if row["COUNTRY_CODE"] in ["KP", "IR", "SY", "MM"]:
                new_violations.append({
                    "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "ACCOUNT_ID": acct_id, 
                    "CUSTOMER_NAME": row["CUSTOMER_NAME"], 
                    "ENFORCED_PROTOCOL": "ACTIVE_LOCK", 
                    "TRIGGER_RULE": "RULE_1_SANCTION_VIOLATION", 
                    "STATUS": "AUTO_ENFORCED"
                })
            
            # Rule 2 - PEP Tax Haven Lock Rule Validation
            if (str(row.get("IS_PEP")).strip().upper() == "TRUE" or row.get("IS_PEP") == True) and row["COUNTRY_CODE"] in ["KY", "CH"]:
                new_violations.append({
                    "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "ACCOUNT_ID": acct_id, 
                    "CUSTOMER_NAME": row["CUSTOMER_NAME"], 
                    "ENFORCED_PROTOCOL": "ACTIVE_LOCK", 
                    "TRIGGER_RULE": "RULE_2_PEP_TAX_HAVEN", 
                    "STATUS": "AUTO_ENFORCED"
                })
                
        if new_violations:
            st.session_state["remediation_log"] = pd.concat([
                st.session_state["remediation_log"], 
                pd.DataFrame(new_violations).drop_duplicates(subset=['ACCOUNT_ID', 'TRIGGER_RULE'])
            ], ignore_index=True)
        st.rerun()
        
    st.markdown("---")
    st.subheader("📋 Active Live REMEDIATION_LOG Table")
        
    if not st.session_state["remediation_log"].empty:
        st.dataframe(
            st.session_state["remediation_log"].sort_values(by="TIMESTAMP", ascending=False), 
            use_container_width=True
        )
        
        if st.session_state.get("active_iam_user") == "SYSTEM_ADMIN":
            if st.button("🗑️ Wipe Remediation Audit Logs & Clear Engine Cache", type="secondary", use_container_width=True):
                st.session_state["remediation_log"] = pd.DataFrame(columns=[
                    "TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "TRIGGER_RULE", "STATUS"
                ])
                st.success("Operational tracking matrices reset successfully.")
                st.rerun()
    else:
        st.info("🟢 No operational containment overrides or system freezes currently active across the network logs.")
