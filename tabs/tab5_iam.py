import streamlit as st

def render(user_profile):
    st.header("🔐 IAM Security & Access Controls")
    st.caption("Role-Based Authentication Simulation - Powered by IDENTITY_ACCESS_MASTER")
    st.markdown("---")
    
    st.subheader("🔁 Fast-Switch Active Identity (Password-Free Simulation)")
    switch_options = {k: f"👤 {v['name']} ({v['role']})" for k, v in st.session_state["iam_directory"].items()}
    selected_switch = st.selectbox("Select an Identity Profile to impersonate system access parameters instantly:", options=list(switch_options.keys()), format_func=lambda x: switch_options[x], index=list(switch_options.keys()).index(st.session_state["active_iam_user"]))
    
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
        st.info(", ".join([f"[{t}]" for t in user_profile['tabs']]))
    with c2:
        st.markdown("### Authorized Access")
        for item in user_profile["permitted"]: st.markdown(f"- `✔️` {item}")
        for item in user_profile["restricted"]: st.markdown(f"- `🛑` {item}")
        
    st.markdown("---")
    st.subheader("👥 User Directory & Management")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("### ➕ Add New User")
        new_user_id = st.text_input("Username / Unique ID")
        new_disp_name = st.text_input("Display Name")
        new_role = st.selectbox("Access Role", ["SYSTEM_ADMIN", "SENIOR_AUDITOR", "COMPLIANCE_ANALYST", "JUNIOR_CLERK"], index=3)
        if st.button("➕ Provision Identity Profile", type="primary", use_container_width=True):
            if new_user_id and new_disp_name:
                tab_rules = ["Account Directory Lookup", "IAM Security & Access Controls"]
                if new_role == "SYSTEM_ADMIN": tab_rules = ["Operational Dashboard", "Conversational CoCo Copilot", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
                st.session_state["iam_directory"][new_user_id] = {"name": new_disp_name, "role": new_role, "clearance": "L1_BASIC", "dept": "Operations", "permitted": ["Basic Read"], "restricted": ["Admin locked"], "tabs": tab_rules}
                st.success("Successfully provisioned identity!"); st.rerun()
    with m2:
        st.markdown("### 🔄 Toggle User Status")
        target_toggle_user = st.selectbox("Select User Profile Node", list(st.session_state["iam_directory"].keys()))
        if st.button("Revoke System Access Link", use_container_width=True):
            st.session_state["iam_directory"][target_toggle_user]["tabs"] = ["IAM Security & Access Controls"]
            st.warning("Access configuration streams revoked."); st.rerun()
