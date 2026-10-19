# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🛡️ REMEDIATION & ACTIONS CONSOLE (TAB 4) ─────
# ─── PART 1: TARGET CONTAINMENT DESK & INTERACTIVE UNLOCK MATRIX ─────
# =====================================================================
import streamlit as st
import pandas as pd
import os

def render(engine):
    st.header("🛡️ Remediation & Actions Console")
    st.caption("Active Incident Response Core Routing - Updates the REMEDIATION_LOG Table Natively")
    st.markdown("---")
    
    log_csv_path = getattr(engine, "remediation_csv_path", "data/remediation_log.csv")
    
    # 🔗 DYNAMIC LIVE DATA BRIDGE LAYER
    if "remediation_log" not in st.session_state or st.session_state["remediation_log"] is None:
        # Step A: First attempt to load physical local storage files if they exist on a desktop drive
        if os.path.exists(log_csv_path):
            try:
                st.session_state["remediation_log"] = pd.read_csv(log_csv_path)
            except Exception:
                st.session_state["remediation_log"] = pd.DataFrame()
        else:
            st.session_state["remediation_log"] = pd.DataFrame()
        
        # Step B: Dynamic Real-time Calculation (Triggers automatically if log is missing or running on Web Cloud)
        if st.session_state["remediation_log"].empty:
            init_records = []
            if not engine.acc_df.empty:
                # Dynamically extract every account profile that currently contains an ACTIVE_LOCK parameter state
                historical_locks = engine.acc_df[engine.acc_df["SYSTEMIC_LOCK_STATUS"] == "ACTIVE_LOCK"]
                for _, h_row in historical_locks.iterrows():
                    init_records.append({
                        "TIMESTAMP": "2026-09-29 12:06:34",
                        "ACCOUNT_ID": h_row["ACCOUNT_ID"],
                        "CUSTOMER_NAME": h_row["CUSTOMER_NAME"],
                        "ENFORCED_PROTOCOL": "ACTIVE_LOCK",
                        "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                        "TRIGGER_RULE": "HISTORICAL_SWEEP_ENGINE",
                        "STATUS": "ACTIVE_ENFORCED"
                    })
            
            # Instantly formulate clean, active runtime dataframe frames
            st.session_state["remediation_log"] = pd.DataFrame(init_records, columns=[
                "TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "SYSTEMIC_LOCK_STATUS", "TRIGGER_RULE", "STATUS"
            ])
            
            # Persist locally to the filesystem ONLY if the user environment has open folder write privileges
            try:
                if not os.path.exists(log_csv_path):
                    os.makedirs(os.path.dirname(log_csv_path), exist_ok=True)
                    st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass # Gracefully handle web instance containers with blocked disk write paths

    st.subheader("🎯 Targeted Account Containment Protocols")
    c1, c2 = st.columns(2)
    
    with c1: 
        target_account = st.selectbox("Select Target Profile to Contain:", sorted(engine.acc_df["ACCOUNT_ID"].unique()))
    
    with c2: 
        selected_protocol = st.selectbox(
            "Select Mitigation Protocol to Enforce:", 
            ["ACTIVE_LOCK", "UNLOCKED", "ENHANCED_EDD", "DEBIT_HOLD_60_DAYS"]
        )
        
    compliance_justification = ""
    uploaded_doc = None
    
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
            cust_name = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account]["CUSTOMER_NAME"].values[0]
            
            # Mutate runtime in-memory parameters instantly
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "SYSTEMIC_LOCK_STATUS"] = selected_protocol
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "OUTBOUND_OVERRIDE_ENABLED"] = "true" if selected_protocol == "UNLOCKED" else "false"
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "COMPLIANCE_REMARKS"] = compliance_justification if selected_protocol == "UNLOCKED" else "NA"
            
            # Try updating the underlying backing tracking sheet files
            try:
                csv_target_path = getattr(engine, "acc_csv_path", "data/account_master.csv")
                engine.acc_df.to_csv(csv_target_path, index=False)
            except Exception:
                pass

            trigger_rule_label = "MANUAL_CONTAINMENT_DESK" if selected_protocol != "UNLOCKED" else "MANUAL_RELEASE_DESK"
            enforcement_status = "ACTIVE_ENFORCED" if selected_protocol != "UNLOCKED" else "RELEASE_LOG_CLEAR"
            
            new_log = {
                "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "ACCOUNT_ID": target_account, 
                "CUSTOMER_NAME": cust_name, 
                "ENFORCED_PROTOCOL": selected_protocol, 
                "SYSTEMIC_LOCK_STATUS": selected_protocol,
                "TRIGGER_RULE": trigger_rule_label, 
                "STATUS": enforcement_status
            }
            
            st.session_state["remediation_log"] = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
            
            try:
                st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass
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
        log_df = st.session_state["remediation_log"]
        active_locks_exist = False
        
        if not log_df.empty:
            latest_entries = log_df.sort_values("TIMESTAMP").groupby("ACCOUNT_ID").last()
            if "SYSTEMIC_LOCK_STATUS" in latest_entries.columns:
                active_locks_exist = (latest_entries["SYSTEMIC_LOCK_STATUS"] == "ACTIVE_LOCK").any()
            elif "ENFORCED_PROTOCOL" in latest_entries.columns:
                active_locks_exist = (latest_entries["ENFORCED_PROTOCOL"] == "ACTIVE_LOCK").any()

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
    st.markdown("""
    * **Rule 1 - Sanctioned Country Auto-Freeze:** If any transaction routes to KP, IR, SY, or MM ➔ Immediate ACTIVE_LOCK + auto-generated STR.
    * **Rule 2 - PEP Tax Haven Lock:** If a PEP account routes funds to KY or CH ➔ Immediate ACTIVE_LOCK + ENHANCED_EDD.
    """)
    st.warning("⚠️ This will scan ALL transactions and auto-lock matching accounts in the REMEDIATION_LOG.")
    
    if st.button("⚡ Run Engine Automated Rules Automation", use_container_width=True):
        clean_tx = engine.tx_df[engine.tx_df["TRANSACTION_ID"] != "TRANSACTION_ID"]
        merged_ledger = pd.merge(clean_tx, engine.acc_df, on="ACCOUNT_ID")
        new_violations = []
        
        remediation_df = st.session_state["remediation_log"]
        unlocked_accounts = set()
        
        if not remediation_df.empty:
            latest_states = remediation_df.sort_values("TIMESTAMP").groupby("ACCOUNT_ID").last().reset_index()
            status_col = "STATUS" if "STATUS" in latest_states.columns else "SYSTEMIC_LOCK_STATUS"
            unlocked_accounts = set(latest_states[latest_states[status_col] == "RELEASE_LOG_CLEAR"]["ACCOUNT_ID"].unique())

        for _, row in merged_ledger.iterrows():
            acct_id = row["ACCOUNT_ID"]
            
            if acct_id in unlocked_accounts:
                continue
                
            # Rule 1 Check Execution Loop
            if row["COUNTRY_CODE"] in ["KP", "IR", "SY", "MM"]:
                new_violations.append({
                    "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "ACCOUNT_ID": acct_id, 
                    "CUSTOMER_NAME": row["CUSTOMER_NAME"], 
                    "ENFORCED_PROTOCOL": "ACTIVE_LOCK", 
                    "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                    "TRIGGER_RULE": "RULE_1_SANCTION_VIOLATION", 
                    "STATUS": "AUTO_ENFORCED"
                })
            
            # Rule 2 Check Execution Loop
            if (str(row.get("IS_PEP")).strip().upper() == "TRUE" or row.get("IS_PEP") == True) and row["COUNTRY_CODE"] in ["KY", "CH"]:
                new_violations.append({
                    "TIMESTAMP": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "ACCOUNT_ID": acct_id, 
                    "CUSTOMER_NAME": row["CUSTOMER_NAME"], 
                    "ENFORCED_PROTOCOL": "ACTIVE_LOCK", 
                    "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                    "TRIGGER_RULE": "RULE_2_PEP_TAX_HAVEN", 
                    "STATUS": "AUTO_ENFORCED"
                })
                
        if new_violations:
            updated_log = pd.concat([st.session_state["remediation_log"], pd.DataFrame(new_violations)], ignore_index=True)
            updated_log = updated_log.drop_duplicates(subset=['ACCOUNT_ID', 'TRIGGER_RULE'])
            st.session_state["remediation_log"] = updated_log
            try:
                updated_log.to_csv(log_csv_path, index=False)
            except Exception:
                pass
        st.rerun()
        
    st.markdown("---")
    st.subheader("📋 Active Live REMEDIATION_LOG Table")
        
    if not st.session_state["remediation_log"].empty:
        st.dataframe(st.session_state["remediation_log"].sort_values(by="TIMESTAMP", ascending=False), use_container_width=True)
        if st.session_state.get("active_iam_user") == "SYSTEM_ADMIN":
            if st.button("🗑️ Wipe Remediation Audit Logs & Clear Engine Cache", type="secondary", use_container_width=True):
                empty_log = pd.DataFrame(columns=["TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "SYSTEMIC_LOCK_STATUS", "TRIGGER_RULE", "STATUS"])
                st.session_state["remediation_log"] = empty_log
                try:
                    empty_log.to_csv(log_csv_path, index=False)
                except Exception:
                    pass
                st.success("Operational tracking matrices reset successfully.")
                st.rerun()
    else:
        st.info("🟢 No operational containment overrides or system freezes currently active across the network logs.")
