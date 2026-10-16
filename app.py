# =====================================================================
# ─── RISK-GEMMA4-AGENT: CENTRAL ROUTING CORE HUB & SIDEBAR LIFECYCLE
# =====================================================================
import streamlit as st
import os
import pandas as pd

st.set_page_config(
    page_title="Risk-Gemma4-Agent Panel", 
    page_icon="🛡️", 
    layout="wide"
)

# ─── 🔑 CENTRAL ENVELOPE AUTHENTICATION LAYER ───
st.sidebar.header("🔑 Authentication")
user_key = st.sidebar.text_input(
    "Enter Google API Key", 
    type="password", 
    help="Provide your Gemini API Key from Google AI Studio. It is safely isolated in session memory."
)

if user_key:
    if st.session_state.get("active_key") != user_key:
        st.session_state["active_key"] = user_key
        st.cache_resource.clear()
    os.environ["GOOGLE_API_KEY"] = user_key

if not os.environ.get("GOOGLE_API_KEY"):
    st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
    st.info("💡 **Welcome to the Workspace!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemma 4 pipelines.")
    st.stop()

# ─── ⚙️ SYSTEM CORE INFRASTRUCTURE LOADERS ───
from gemma4_engine import FraudCopilotEngine

@st.cache_resource
def init_engine(): 
    return FraudCopilotEngine()

try: 
    engine = init_engine()
except Exception as e: 
    st.error(f"❌ Initialization Error: {e}")
    st.stop()

# ─── 🎛️ GLOBAL CONTROL PARAMETERS PANEL ───
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")

def handle_threshold_shift():
    if "audit_data_cache" in st.session_state:
        del st.session_state["audit_data_cache"]

if "current_threshold" not in st.session_state: 
    st.session_state["current_threshold"] = 5000000

min_threshold = st.sidebar.slider(
    "Cross-Border Alert Threshold (₹)", 
    1000000, 10000000, 
    key="current_threshold", 
    step=500000,
    on_change=handle_threshold_shift
)

# ─── 🧠 REASONING ENGINE CONFIGURATION HUB ───
st.sidebar.markdown("---")
st.sidebar.header("🧠 Reasoning Engine Layout")

thinking_options = {
    "⚡ Minimal (Fastest / Direct)": "MINIMAL", 
    "🔴 High (Full Reasoning Cluster)": "HIGH"
}
selected_label = st.sidebar.selectbox(
    "Gemma 4 Thinking Tier:", 
    list(thinking_options.keys()), 
    index=0
)
st.session_state["active_thinking_level"] = thinking_options[selected_label]

# ─── 🧹 SYSTEM CACHE OPERATION UTILITIES ───
st.sidebar.markdown("---")
st.sidebar.header("⚙️ System Utilities")

if st.sidebar.button("🧹 Clear System Cache & Reset Chat", use_container_width=True, type="secondary"):
    st.cache_resource.clear()
    st.session_state.messages = []
    if "audit_data_cache" in st.session_state:
        del st.session_state["audit_data_cache"]
    st.success("🔄 Session cache cleared successfully!")
    st.rerun()

# ─── 📊 GLOBAL OPERATIONAL STATE LIFECYCLES ───
if "messages" not in st.session_state: st.session_state.messages = []
if "report_review_status" not in st.session_state: st.session_state["report_review_status"] = "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER"
if "remediation_log" not in st.session_state: st.session_state["remediation_log"] = pd.DataFrame(columns=["TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "TRIGGER_RULE", "STATUS"])

# ─── 🔐 INITIALIZE IAM REGISTRY MULTI-ROLE DATA ───
if "iam_logged_in" not in st.session_state: st.session_state["iam_logged_in"] = False
if "active_iam_user" not in st.session_state: st.session_state["active_iam_user"] = "admin_srinivas"

if "iam_directory" not in st.session_state:
    st.session_state["iam_directory"] = {
        "admin_srinivas": {
            "name": "Appala Srinivas Tanakala", "role": "SYSTEM_ADMIN", "clearance": "Level 4 - Full Access", "dept": "IT Security & Infrastructure",
            "permitted": ["Unrestricted system access", "Manage IAM users", "Modify clearance levels", "System configuration overrides"], "restricted": ["No restrictions; full system access"],
            "tabs": ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
        },
        "auditor_priya": {
            "name": "Priya Patel", "role": "SENIOR_AUDITOR", "clearance": "Level 3 - Audit Review", "dept": "Risk & Compliance Unit",
            "permitted": ["Execute compliance audit pipeline", "View corporate accounts directory", "Verify transaction registries"], "restricted": ["Interact with conversational AI engines", "Execute manual holds", "File STR payloads to FIU-IND Portal"],
            "tabs": ["Operational Dashboard", "Account Directory Lookup", "IAM Security & Access Controls"]
        },
        "analyst_anita": {
            "name": "Anita Sharma", "role": "COMPLIANCE_ANALYST", "clearance": "Level 2 - Intelligence Access", "dept": "Financial Crime Unit",
            "permitted": ["Execute compliance audit pipeline", "Access Conversational Gemma4", "Lookup Account Directory profiles", "Access Remediation Desk"], "restricted": ["System configuration overrides", "Modify system variables"],
            "tabs": ["Operational Dashboard", "Conversational Gemma4", "Account Directory Lookup", "Remediation & Actions Console", "IAM Security & Access Controls"]
        },
        "clerk_rajesh": {
            "name": "Rajesh Kumar", "role": "JUNIOR_CLERK", "clearance": "Level 1 - Basic Read", "dept": "Operations Backoffice",
            "permitted": ["Monitor dashboard metrics data flows", "Verify basic compliance logs"], 
            "restricted": ["Interact with conversational AI engines", "Access customer registries", "Execute containment protocols", "Modify security structures", "Access IAM controller configuration matrices"],
            # 💡 ABSOLUTE LOCK POLICY: Restricted entirely to Tab 1 only (No access to Tab 5 IAM console)
            "tabs": ["Operational Dashboard"]
        }
    }

# ─── 🚪 SIDEBAR INTEGRATED LOGIN & LOGOUT HUB ───
st.sidebar.markdown("---")
st.sidebar.header("🔐 Session Management")

if not st.session_state["iam_logged_in"]:
    selector_map = {k: f"👤 {v['name']} ({v['role']})" for k, v in st.session_state["iam_directory"].items()}
    chosen_login = st.sidebar.selectbox("Select Profile Node to Authenticate:", options=list(selector_map.keys()), format_func=lambda x: selector_map[x])
    
    if st.sidebar.button("🔓 Login & Mount Workspace", type="primary", use_container_width=True):
        st.session_state["active_iam_user"] = chosen_login
        st.session_state["iam_logged_in"] = True
        st.sidebar.success("Authentication Mounted!")
        st.rerun()
        
    st.title("🛡️ Identity Access Restrictions Gate")
    st.warning("💡 **Terminal Locked Out:** Please choose an identity profile via the sidebar panel on the left edge and click **Login** to display the authorized workspace data channels.")
    st.stop()
else:
    active_profile = st.session_state["iam_directory"][st.session_state["active_iam_user"]]
    st.sidebar.markdown(f"**Authenticated Identity:**")
    st.sidebar.code(f"👤 {active_profile['name']}\n💼 {active_profile['role']}\n🏷️ {active_profile['clearance']}")
    
    if st.sidebar.button("🚪 Terminate Session & Logout", type="secondary", use_container_width=True):
        st.session_state["iam_logged_in"] = False
        st.sidebar.warning("Session Cleared.")
        st.rerun()

# ─── 🛡️ DYNAMIC ROLE-BASED ACCESS CONTROL TAB ROUTER ───
active_user_key = st.session_state["active_iam_user"]
user_profile = st.session_state["iam_directory"][active_user_key]
visible_tabs_list = user_profile["tabs"]

# Generate available tabs based on the active user profile's access list
generated_tabs = st.tabs([f"🔒 {t}" if t != "IAM Security & Access Controls" else f"🔐 {t}" for t in visible_tabs_list])
tab_mapping = dict(zip(visible_tabs_list, generated_tabs))

# ─── 📁 MODULAR PANEL INJECTIONS ───
from tabs import tab1_dashboard, tab2_gemma4, tab3_registry, tab4_reremediation, tab5_iam

if "Operational Dashboard" in tab_mapping:
    with tab_mapping["Operational Dashboard"]: 
        tab1_dashboard.render(engine, min_threshold)

if "Conversational Gemma4" in tab_mapping:
    with tab_mapping["Conversational Gemma4"]: 
        tab2_gemma4.render(engine, min_threshold)

if "Account Directory Lookup" in tab_mapping:
    with tab_mapping["Account Directory Lookup"]: 
        tab3_registry.render(engine)

if "Remediation & Actions Console" in tab_mapping:
    with tab_mapping["Remediation & Actions Console"]: 
        tab4_reremediation.render(engine)

if "IAM Security & Access Controls" in tab_mapping:
    with tab_mapping["IAM Security & Access Controls"]: 
        tab5_iam.render(user_profile)
