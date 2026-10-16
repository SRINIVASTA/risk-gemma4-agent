# =====================================================================
# ─── RISK-GEMMA4-AGENT: 🔐 IAM SECURITY & ACCESS CONTROLS (TAB 5) ────
# =====================================================================
import streamlit as st
import pandas as pd

def render(user_profile):
    st.header("🔐 IAM Security & Access Controls")
    st.caption("Role-Based Authentication Simulation - Powered by IDENTITY_ACCESS_MASTER")
    st.markdown("---")
    
    # 👤 PROFILE IDENTITY PROTOCOLS CARD & LOGOUT
    c1, c2 = st.columns()
    
    with c1:
        st.subheader(f"👤 {user_profile['name']}")
        st.markdown(f"**Role:** `{user_profile['role']}` &nbsp;|&nbsp; **Clearance:** `{user_profile['clearance']}` &nbsp;|&nbsp; **Department:** `{user_profile['dept']}`")
        st.markdown("📂 **Accessible Dashboard Workspace Channels:**")
        st.info(", ".join([f"[{t}]" for t in user_profile['tabs']]))
        
    with c2:
        st.markdown("### Session Management")
        if st.button("🚪 Terminate Session & Logout", type="secondary", use_container_width=True):
            st.session_state["iam_logged_in"] = False
            st.warning("Session destroyed successfully.")
            st.rerun()

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

    st.markdown("---")
    
    # 👥 USER DIRECTORY & MANAGEMENT FOR ADMINISTRATORS
    st.subheader("👥 User Directory & Management Dashboard")
    m1, m2 = st.columns(2)
    
    with m1:
        st.markdown("### ➕ Add New User Profile")
        new_user_id = st.text_input("Username / Unique ID", placeholder="e.g., clerk_suresh")
        new_disp_name = st.text_input("Display Name", placeholder="e.g., Suresh Kumar")
        new_role = st.selectbox("Access Role Mappings Profile:", ["SYSTEM_ADMIN", "SENIOR_AUDITOR", "COMPLIANCE_ANALYST", "JUNIOR_CLERK"], index=3)
        new_clearance = st.selectbox("Clearance Assignment Matrix:", ["L4_FULL_ACCESS", "L3_AUDIT_REVIEW", "L2_INTEL_ACCESS", "L1_BASIC"], index=3)
        new_dept = st.text_input("Department Node Link", value="Operations Backoffice")
        
        if st.button("➕ Provision Identity Profile Node", type="primary", use_container_width=True):
            if new_user_id and new_disp_name:
                # ─── 💡 ALIGNED ROLE BOUNDARIES POLICIES ───
                if new_role == "SYSTEM_ADMIN":
                    tab_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                elif new_role == "SENIOR_AUDITOR":
                    tab_rules = ["Operational Dashboard", "Account Directory Lookup", "IAM Security & Access Controls"]
                elif new_role == "COMPLIANCE_ANALYST":
                    tab_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                else:  # JUNIOR_CLERK
                    # Strictly restricted to monitoring main dashboard metrics only
                    tab_rules = ["Operational Dashboard", "IAM Security & Access Controls"]
                
                st.session_state["iam_directory"][new_user_id] = {
                    "name": new_disp_name, "role": new_role, "clearance": new_clearance.replace("_", " ").title(), "dept": new_dept,
                    "permitted": ["Assigned by Role Mapping Policy Core"], "restricted": ["Elevated elements restricted by policy hierarchy"],
                    "tabs": tab_rules
                }
                st.success(f"Identity context provisioned for {new_disp_name}!")
                st.rerun()
            else:
                st.error("Username and Display Name metrics are required.")

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
