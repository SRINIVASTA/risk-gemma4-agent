import streamlit as st

def render(user_profile):
    st.header("🔐 IAM Security & Access Controls")
    st.caption("Role-Based Authentication Simulation - Powered by IDENTITY_ACCESS_MASTER")
    st.markdown("---")
    
    # 🔁 Fast-Switch Active Identity (Password-Free Simulation)
    st.subheader("🔁 Fast-Switch Active Identity (Password-Free Simulation)")
    switch_options = {k: f"👤 {v['name']} ({v['role']})" for k, v in st.session_state["iam_directory"].items()}
    selected_switch = st.selectbox(
        "Select an Identity Profile to impersonate system access parameters instantly:", 
        options=list(switch_options.keys()), 
        format_func=lambda x: switch_options[x], 
        index=list(switch_options.keys()).index(st.session_state["active_iam_user"])
    )
    
    if selected_switch != st.session_state["active_iam_user"]:
        st.session_state["active_iam_user"] = selected_switch
        st.success(f"Identity swapped context to **{st.session_state['iam_directory'][selected_switch]['name']}**!")
        st.rerun()
        
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"👤 {user_profile['name']}")
        st.write(f"**Role:** `{user_profile['role']}`")
        st.write(f"**Clearance:** `{user_profile['clearance']}`")
        st.write(f"**Department:** {user_profile['dept']}")
        
        st.markdown("📂 **Accessible Tabs:**")
        st.info(", ".join([f"[{t}]" for t in user_profile['tabs']]))
    with c2:
        st.markdown("### Authorized Access")
        st.markdown("**✔️ Permitted:**")
        for item in user_profile["permitted"]: 
            st.markdown(f"- `✔️` {item}")
        st.markdown("**🛑 Restricted:**")
        for item in user_profile["restricted"]: 
            st.markdown(f"- `🛑` {item}")
        
    st.markdown("---")
    st.subheader("👥 User Directory & Management")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("### ➕ Add New User")
        new_user_id = st.text_input("Username / Unique ID", placeholder="e.g., jclerk02")
        new_disp_name = st.text_input("Display Name", placeholder="e.g., Suresh Kumar")
        new_role = st.selectbox("Access Role", ["SYSTEM_ADMIN", "SENIOR_AUDITOR", "COMPLIANCE_ANALYST", "JUNIOR_CLERK"], index=3)
        new_clearance = st.selectbox("Clearance Level", ["L4_FULL_ACCESS", "L3_AUDIT_REVIEW", "L2_INTEL_ACCESS", "L1_BASIC"], index=3)
        new_dept = st.text_input("Department Assigned", value="Compliance Operations")
        st.text_input("Initial Password (Disabled in Local Simulation Mode)", value="••••••••", disabled=True)
        
        if st.button("➕ Provision Identity Profile", type="primary", use_container_width=True):
            if new_user_id and new_disp_name:
                # ─── 💡 CORRECTED & ALIGNED DYNAMIC ROLE MAPPING INDEX ───
                if new_role == "SYSTEM_ADMIN":
                    tab_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                elif new_role == "SENIOR_AUDITOR":
                    tab_rules = ["Operational Dashboard", "Account Directory Lookup", "IAM Security & Access Controls"]
                elif new_role == "COMPLIANCE_ANALYST":
                    tab_rules = ["Conversational Gemma4", "Account Directory Lookup", "IAM Security & Access Controls"]
                else:  # JUNIOR_CLERK
                    tab_rules = ["Account Directory Lookup", "IAM Security & Access Controls"]
                    
                st.session_state["iam_directory"][new_user_id] = {
                    "name": new_disp_name,
                    "role": new_role,
                    "clearance": new_clearance.replace("_", " ").title(),
                    "dept": new_dept,
                    "permitted": ["Assigned by Role Mapping Policy"],
                    "restricted": ["Elevated features locked out"],
                    "tabs": tab_rules
                }
                st.success(f"Successfully provisioned structural identity account for {new_disp_name}!")
                st.rerun()
            else:
                st.error("Please fill out both Username and Display Name to provision an identity.")
                
    with m2:
        st.markdown("### 🔄 Toggle User Status")
        target_toggle_user = st.selectbox("Select User Profile Node", list(st.session_state["iam_directory"].keys()))
        action_status = st.radio("Action Protocol", ["🟢 Activate Profile Stream", "🔴 Suspended System Access Link"])
        
        if st.button("Apply Operational Status Change", use_container_width=True):
            if action_status == "🔴 Suspended System Access Link":
                st.session_state["iam_directory"][target_toggle_user]["tabs"] = ["IAM Security & Access Controls"]
                st.warning(f"Profile {target_toggle_user} access configuration streams revoked successfully.")
            else:
                # Restore original corporate tab profiles mapping rules based on role nodes
                u_role = st.session_state["iam_directory"][target_toggle_user]["role"]
                if u_role == "SYSTEM_ADMIN":
                    t_rules = ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                elif u_role == "SENIOR_AUDITOR":
                    t_rules = ["Operational Dashboard", "Account Directory Lookup", "IAM Security & Access Controls"]
                elif u_role == "COMPLIANCE_ANALYST":
                    t_rules = ["Conversational Gemma4", "Account Directory Lookup", "IAM Security & Access Controls"]
                else:
                    t_rules = ["Account Directory Lookup", "IAM Security & Access Controls"]
                    
                st.session_state["iam_directory"][target_toggle_user]["tabs"] = t_rules
                st.success(f"Profile {target_toggle_user} operational channels cleared and verified.")
            st.rerun()
