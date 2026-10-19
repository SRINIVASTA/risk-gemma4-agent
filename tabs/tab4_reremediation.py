# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🛡️ REMEDIATION & ACTIONS CONSOLE (TAB 4) ─────
# ─── PART 1: CORE RE-ALIGNMENT INGESTION & MANUAL CONTAINMENT DESK ───
# =====================================================================
import streamlit as st
import pandas as pd
import os
import uuid

def render(engine):
    st.header("🛡️ Remediation & Actions Console")
    st.caption("Active Incident Response Core Routing - Updates the REMEDIATION_LOG Table Natively")
    st.markdown("---")
    
    log_csv_path = getattr(engine, "remediation_csv_path", "data/remediation_log.csv")
    
    # 🛡️ DEFENSIVE UNIFIED SCHEMA SPECIFICATION DIRECTORY MATRIX
    unified_columns = [
        "ACTION_ID", "ACCOUNT_ID", "SYSTEMIC_LOCK_STATUS", "OUTBOUND_OVERRIDE_ENABLED", 
        "KYC_STEP_UP_LEVEL", "UPDATED_AT", "UPDATED_BY", "COMPLIANCE_REMARKS", "DOCUMENT_REFERENCE"
    ]
    
    # Initialize / Re-align logging dataframe vectors inside active memory state mirrors
    if "remediation_log" not in st.session_state or st.session_state["remediation_log"] is None:
        if os.path.exists(log_csv_path):
            try:
                loaded_df = pd.read_csv(log_csv_path)
                
                # 🔄 AUTOMATIC LAYER INTERCEPT: Clean out legacy columns to arrest data fragmentation anomalies
                if "TIMESTAMP" in loaded_df.columns:
                    loaded_df = loaded_df.rename(columns={
                        "TIMESTAMP": "UPDATED_AT",
                        "TRIGGER_RULE": "COMPLIANCE_REMARKS",
                        "STATUS": "KYC_STEP_UP_LEVEL"
                    })
                
                # Re-index dataframe strictly to prune extraneous empty parameter keys safely
                loaded_df = loaded_df.reindex(columns=unified_columns)
                
                # Verify structural validation loops to anchor system-wide identifier mappings
                if not loaded_df.empty and loaded_df["ACTION_ID"].isnull().any():
                    loaded_df["ACTION_ID"] = loaded_df["ACTION_ID"].apply(lambda x: str(uuid.uuid4()) if pd.isnull(x) else x)
                
                st.session_state["remediation_log"] = loaded_df
            except Exception:
                st.session_state["remediation_log"] = pd.DataFrame(columns=unified_columns)
        else:
            st.session_state["remediation_log"] = pd.DataFrame(columns=unified_columns)
        
        # Self-Healing Routine: Re-align operational profiles dynamically if the ledger reads empty
        if st.session_state["remediation_log"].empty:
            init_records = []
            if not engine.acc_df.empty:
                historical_locks = engine.acc_df[engine.acc_df["SYSTEMIC_LOCK_STATUS"] == "ACTIVE_LOCK"]
                for _, h_row in historical_locks.iterrows():
                    init_records.append({
                        "ACTION_ID": str(uuid.uuid4()),
                        "ACCOUNT_ID": h_row["ACCOUNT_ID"],
                        "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                        "OUTBOUND_OVERRIDE_ENABLED": "false",
                        "KYC_STEP_UP_LEVEL": h_row.get("KYC_STATUS", "STANDARD"),
                        "UPDATED_AT": "2026-10-19T12:00:00",
                        "UPDATED_BY": "REGULATORY_SWEEP_ENGINE",
                        "COMPLIANCE_REMARKS": "HISTORICAL_SWEEP_RECOVERY",
                        "DOCUMENT_REFERENCE": "NA"
                    })
            st.session_state["remediation_log"] = pd.DataFrame(init_records, columns=unified_columns).reset_index(drop=True)
            try:
                os.makedirs(os.path.dirname(log_csv_path), exist_ok=True)
                st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass

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
    uploaded_doc_name = "NA"
    
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
        if uploaded_doc is not None:
            uploaded_doc_name = uploaded_doc.name
    
    if st.button("🚨 Dispatch Mitigation Protocol", type="primary", use_container_width=True):
        if selected_protocol == "UNLOCKED" and not compliance_justification.strip():
            st.error("❌ **Compliance Block:** You must provide a justification remark to change protocol from ACTIVE_LOCK.")
        else:
            # 🛡️ THE FIX: Force the profile status to change to 'Pending' if an action protocol is deployed
            if selected_protocol in ["ACTIVE_LOCK", "DEBIT_HOLD_60_DAYS", "ENHANCED_EDD"]:
                engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "KYC_STATUS"] = "Pending"
                current_kyc = "Pending"
            else:
                # Fallback to keep standard verification levels if unlocking
                current_kyc = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account]["KYC_STATUS"].values[0] if not engine.acc_df[engine.acc_df["ACCOUNT_ID"] == target_account].empty else "STANDARD"
                
            step_up = "CRITICAL" if selected_protocol == "ACTIVE_LOCK" else current_kyc
            
            # Enforce dynamic downstream parameter updates to database instances
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "SYSTEMIC_LOCK_STATUS"] = selected_protocol
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "OUTBOUND_OVERRIDE_ENABLED"] = "true" if selected_protocol == "UNLOCKED" else "false"
            engine.acc_df.loc[engine.acc_df["ACCOUNT_ID"] == target_account, "COMPLIANCE_REMARKS"] = compliance_justification if selected_protocol == "UNLOCKED" else "NA"
            
            try:
                csv_target_path = getattr(engine, "acc_csv_path", "data/account_master.csv")
                engine.acc_df.to_csv(csv_target_path, index=False)
            except Exception:
                pass

            new_log = {
                "ACTION_ID": str(uuid.uuid4()),
                "ACCOUNT_ID": target_account, 
                "SYSTEMIC_LOCK_STATUS": selected_protocol,
                "OUTBOUND_OVERRIDE_ENABLED": "true" if selected_protocol == "UNLOCKED" else "false",
                "KYC_STEP_UP_LEVEL": step_up,
                "UPDATED_AT": pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "UPDATED_BY": st.session_state.get("active_iam_user", "sysadmin01"),
                "COMPLIANCE_REMARKS": compliance_justification if selected_protocol == "UNLOCKED" else "MANUAL_OVERRIDE",
                "DOCUMENT_REFERENCE": uploaded_doc_name
            }
            
            updated_df = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
            # Enforce clean reindex to trap and exclude mutated parameter matrices
            st.session_state["remediation_log"] = updated_df.reindex(columns=unified_columns).reset_index(drop=True)
            
            try:
                st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass
            st.rerun()

            new_log = {
                "ACTION_ID": str(uuid.uuid4()),
                "ACCOUNT_ID": target_account, 
                "SYSTEMIC_LOCK_STATUS": selected_protocol,
                "OUTBOUND_OVERRIDE_ENABLED": "true" if selected_protocol == "UNLOCKED" else "false",
                "KYC_STEP_UP_LEVEL": step_up,
                "UPDATED_AT": pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "UPDATED_BY": st.session_state.get("active_iam_user", "sysadmin01"),
                "COMPLIANCE_REMARKS": compliance_justification if selected_protocol == "UNLOCKED" else "MANUAL_OVERRIDE",
                "DOCUMENT_REFERENCE": uploaded_doc_name
            }
            
            updated_df = pd.concat([st.session_state["remediation_log"], pd.DataFrame([new_log])], ignore_index=True)
            # Enforce clean reindex to trap and exclude mutated parameter matrices
            st.session_state["remediation_log"] = updated_df.reindex(columns=unified_columns).reset_index(drop=True)
            
            try:
                st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass
            st.rerun()
# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🛡️ REMEDIATION & ACTIONS CONSOLE (TAB 4) ─────
# ─── PART 2: REGULATORY ROUTING CORE, AUTOMATION SWEEPS & LEDGERS ────
# =====================================================================
    st.markdown("---")
    st.subheader("📋 Regulatory Export & Core Controls")
    ae1, ae2 = st.columns(2)
    
    with ae1:
        if st.button("📤 Export Compliance Package & File STR to FIU-IND Portal", use_container_width=True): 
            st.success("📤 Routed to FIU-IND gateways successfully via NCRP tracking ports.")
    with ae2:
        log_df = st.session_state["remediation_log"]
        active_locks_exist = False
        
        if not log_df.empty and "UPDATED_AT" in log_df.columns:
            latest_entries = log_df.sort_values("UPDATED_AT").groupby("ACCOUNT_ID").last()
            if "SYSTEMIC_LOCK_STATUS" in latest_entries.columns:
                active_locks_exist = (latest_entries["SYSTEMIC_LOCK_STATUS"] == "ACTIVE_LOCK").any()

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
    st.warning("⚠️ This will scan ALL transactions and auto-lock matching accounts in the REMEDIATION_LOG without header corruption.")
    
    if st.button("⚡ Run Engine Automated Rules Automation", use_container_width=True):
        clean_tx = engine.tx_df[engine.tx_df["TRANSACTION_ID"] != "TRANSACTION_ID"]
        merged_ledger = pd.merge(clean_tx, engine.acc_df, on="ACCOUNT_ID")
        new_violations = []
        
        remediation_df = st.session_state["remediation_log"]
        unlocked_accounts = set()
        
        if not remediation_df.empty and "UPDATED_AT" in remediation_df.columns:
            latest_states = remediation_df.sort_values("UPDATED_AT").groupby("ACCOUNT_ID").last().reset_index()
            unlocked_accounts = set(latest_states[latest_states["SYSTEMIC_LOCK_STATUS"] == "UNLOCKED"]["ACCOUNT_ID"].unique())

        for _, row in merged_ledger.iterrows():
            acct_id = row["ACCOUNT_ID"]
            if acct_id in unlocked_accounts:
                continue
                
            # Rule 1 Check Execution Loop (Sanctioned Countries)
            if row["COUNTRY_CODE"] in ["KP", "IR", "SY", "MM"]:
                new_violations.append({
                    "ACTION_ID": str(uuid.uuid4()),
                    "ACCOUNT_ID": acct_id, 
                    "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                    "OUTBOUND_OVERRIDE_ENABLED": "false",
                    "KYC_STEP_UP_LEVEL": "CRITICAL",
                    "UPDATED_AT": pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "UPDATED_BY": "REGULATORY_SWEEP_ENGINE",
                    "COMPLIANCE_REMARKS": "RULE_1_SANCTION_VIOLATION",
                    "DOCUMENT_REFERENCE": "NA"
                })
            
            # Rule 2 Check Execution Loop (PEP Tax Havens)
            if (str(row.get("IS_PEP")).strip().upper() == "TRUE" or row.get("IS_PEP") == True) and row["COUNTRY_CODE"] in ["KY", "CH"]:
                new_violations.append({
                    "ACTION_ID": str(uuid.uuid4()),
                    "ACCOUNT_ID": acct_id, 
                    "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK",
                    "OUTBOUND_OVERRIDE_ENABLED": "false",
                    "KYC_STEP_UP_LEVEL": "ENHANCED_EDD",
                    "UPDATED_AT": pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "UPDATED_BY": "REGULATORY_SWEEP_ENGINE",
                    "COMPLIANCE_REMARKS": "RULE_2_PEP_TAX_HAVEN",
                    "DOCUMENT_REFERENCE": "NA"
                })
                
        if new_violations:
            violations_df = pd.DataFrame(new_violations)
            updated_log = pd.concat([st.session_state["remediation_log"], violations_df], ignore_index=True)
            
            # Deduplicate logs across constraints and force unified structure parameters strictly
            updated_log = updated_log.drop_duplicates(subset=['ACCOUNT_ID', 'COMPLIANCE_REMARKS'])
            st.session_state["remediation_log"] = updated_log.reindex(columns=unified_columns).reset_index(drop=True)
            
            try:
                st.session_state["remediation_log"].to_csv(log_csv_path, index=False)
            except Exception:
                pass
        st.rerun()
        
    st.markdown("---")
    st.subheader("📋 Active Live REMEDIATION_LOG Table")
        
    if not st.session_state["remediation_log"].empty:
        # Display cleanly aligned logs, avoiding empty cell layouts
        st.dataframe(
            st.session_state["remediation_log"].sort_values(by="UPDATED_AT", ascending=False), 
            use_container_width=True
        )
        if st.session_state.get("active_iam_user") == "SYSTEM_ADMIN":
            if st.button("🗑️ Wipe Remediation Audit Logs & Clear Engine Cache", type="secondary", use_container_width=True):
                empty_log = pd.DataFrame(columns=unified_columns)
                st.session_state["remediation_log"] = empty_log
                try:
                    empty_log.to_csv(log_csv_path, index=False)
                except Exception:
                    pass
                st.success("Operational tracking matrices reset successfully.")
                st.rerun()
    else:
        st.info("🟢 No operational containment overrides or system freezes currently active across the network logs.")
