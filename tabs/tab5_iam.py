# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🔐 IAM SECURITY & ACCESS CONTROLS (TAB 5) ────
# ─── PART 1: IDENTITY DESK & READ-ONLY ACCESS CONTROLS ───────────────
# =====================================================================
import streamlit as st
import pandas as pd

def render(user_profile):
    st.header("🔐 IAM Security & Access Controls")
    st.caption("Role-Based Authentication Simulation - Powered by IDENTITY_ACCESS_MASTER")
    st.markdown("---")
    
    # 👤 PROFILE IDENTITY PROTOCOLS CARD
    st.subheader(f"👤 Active Profile Node: {user_profile['name']}")
    st.markdown(f"**Role Registry:** `{user_profile['role']}` &nbsp;|&nbsp; **Clearance Level:** `{user_profile['clearance']}` &nbsp;|&nbsp; **Department Node:** `{user_profile['dept']}`")
    
    st.markdown("📂 **Accessible Dashboard Workspace Channels:**")
    st.info(", ".join([f"[{t}]" for t in user_profile['tabs']]))
        
    st.markdown("---")
    
    # PERMISSIONS SUMMARY GRID
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("### Authorized System Actions")
        for item in user_profile["permitted"]:
            st.markdown(f"- `✔️` {item}")
    with p2:
        st.markdown("### Enforced System Restrictions")
        for item in user_profile["restricted"]:
            st.markdown(f"- `🛑` {item}")
# =====================================================================
# ─── PART 2: DYNAMIC PROVISIONING HUB & ACTION WRITE-LOCK PROTOCOLS ──
# =====================================================================
    st.markdown("---")
    st.subheader("👥 User Directory & Management Dashboard")
    
    m1, m2 = st.columns(2)
    
    with m1:
        # 🔒 CRITICAL SECURITY LOCK: Grant write access ONLY to the System Administrator
        if user_profile['role'] == "SYSTEM_ADMIN":
            st.markdown("### ➕ Add New User Profile")
            new_user_id = st.text_input("Username / Unique ID", placeholder="e.g., clerk_suresh")
            new_disp_name = st.text_input("Display Name", placeholder="e.g., Suresh Kumar")
            new_role = st.selectbox("Access Role Mappings Profile:", ["SYSTEM_ADMIN", "SENIOR_AUDITOR", "COMPLIANCE_ANALYST", "JUNIOR_CLERK"], index=3)
            new_clearance = st.selectbox("Clearance Assignment Matrix:", ["L4_FULL_ACCESS", "L3_AUDIT_REVIEW", "L2_INTEL_ACCESS", "L1_BASIC"], index=3)
            new_dept = st.text_input("Department Node Link", value="Operations Backoffice")
            
            if st.button("➕ Provision Identity Profile Node", type="primary", use_container_width=True):
                if new_user_id and new_disp_name:
                    if new_role == "SYSTEM_ADMIN":
                        tab_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                    elif new_role == "SENIOR_AUDITOR":
                        tab_rules = ["Operational Dashboard", "Account Directory Lookup", "IAM Security & Access Controls"]
                    elif new_role == "COMPLIANCE_ANALYST":
                        tab_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                    else:  # JUNIOR_CLERK
                        tab_rules = ["Operational Dashboard"]
                    
                    st.session_state["iam_directory"][new_user_id] = {
                        "name": new_disp_name, "role": new_role, "clearance": new_clearance.replace("_", " ").title(), "dept": new_dept,
                        "permitted": ["Assigned by Role Mapping Policy Core"], "restricted": ["Elevated elements restricted by policy hierarchy"],
                        "tabs": tab_rules
                    }
                    st.success(f"Identity context provisioned for {new_disp_name}!")
                    st.rerun()
                else:
                    st.error("Username and Display Name metrics are required.")
        else:
            # 🛑 READ-ONLY ENFORCEMENT NOTICE FOR AUDITORS & CLERKS
            st.markdown("### ➕ User Provisioning Desk")
            st.warning("🛡️ **Read-Only Access Enforced:** Your active role profile does not possess write privileges to modify identity directories, provision new system nodes, or alter clearance configurations.")
            st.info("💡 *Audit Trail Rule: Auditors can examine the active directory entries table in the right-hand panel to verify user permissions lineage, but changes require a SYSTEM_ADMIN credential token override.*")

    with m2:
        st.markdown("### 🔄 Active Identity Profile Index")
        summary_rows = []
        for key, data in st.session_state["iam_directory"].items():
            summary_rows.append({
                "User Node": key,
                "Name Registry": data["name"],
                "Assigned Role": data["role"],
                "Unlocked Tabs Count": len(data["tabs"])
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
