# =====================================================================
# ─── RISK-GEMMA4-AGENT: CENTRAL ROUTING CORE HUB & LIFECYCLE CONTROLLER
# =====================================================================
import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Risk-Gemma4-Agent Panel", page_icon="🛡️", layout="wide")

# ─── 🔑 CENTRAL ENVELOPE AUTHENTICATION LAYER ───
st.sidebar.header("🔑 Authentication")
user_key = st.sidebar.text_input("Enter Google API Key", type="password", help="Provide your Gemini API Key.")

if user_key:
    if st.session_state.get("active_key") != user_key:
        st.session_state["active_key"] = user_key
        st.cache_resource.clear()
    os.environ["GOOGLE_API_KEY"] = user_key

if not os.environ.get("GOOGLE_API_KEY"):
    st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
    st.info("💡 **Welcome to the Workspace!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemma 4 pipelines.")
    st.stop()

from gemma4_engine import FraudCopilotEngine

@st.cache_resource
def init_engine(): return FraudCopilotEngine()

try: engine = init_engine()
except Exception as e: st.error(f"❌ Initialization Error: {e}"); st.stop()

# ─── 🎛️ GLOBAL CONTROL PARAMETERS PANEL ───
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")

if "current_threshold" not in st.session_state: st.session_state["current_threshold"] = 5000000
min_threshold = st.sidebar.slider("Cross-Border Alert Threshold (₹)", 1000000, 10000000, key="current_threshold", step=500000)

thinking_options = {"⚡ Minimal (Fastest / Direct)": "MINIMAL", "🔴 High (Full Reasoning Cluster)": "HIGH"}
selected_label = st.sidebar.selectbox("Gemma 4 Thinking Tier:", list(thinking_options.keys()), index=0)
st.session_state["active_thinking_level"] = thinking_options[selected_label]

# ─── 📊 GLOBAL OPERATIONAL STATE LIFECYCLES ───
if "messages" not in st.session_state: st.session_state.messages = []
if "report_review_status" not in st.session_state: st.session_state["report_review_status"] = "⚠️ PENDING HUMAN SIGN-OFF BY COMPLIANCE OFFICER"
if "remediation_log" not in st.session_state: st.session_state["remediation_log"] = pd.DataFrame(columns=["TIMESTAMP", "ACCOUNT_ID", "CUSTOMER_NAME", "ENFORCED_PROTOCOL", "TRIGGER_RULE", "STATUS"])

# ─── 🔐 INITIALIZE REAL-TIME ACTIVE LOGGED WORKSPACE STATES ───
if "iam_logged_in" not in st.session_state:
    st.session_state["iam_logged_in"] = False

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
            "restricted": ["Interact with conversational AI engines", "Access customer registries", "Execute containment protocols", "Modify system parameters"],
            # 💡 FIXED WORKSPACE BOUNDARY: Junior Clerk restricted to Operational Dashboard and IAM Console only
            "tabs": ["Operational Dashboard", "IAM Security & Access Controls"]
        }
    }

if "active_iam_user" not in st.session_state: 
    st.session_state["active_iam_user"] = "admin_srinivas"

# ─── 🚀 LOGIN GATEWAY DISPATCH CONTROLLER ───
if not st.session_state["iam_logged_in"]:
    st.title("🔐 IAM Security Access Portal")
    st.info("Welcome to Identity Management Simulation. Select an identity below to log into the terminal workspace.")
    
    selector_map = {k: f"👤 {v['name']} ({v['role']})" for k, v in st.session_state["iam_directory"].items()}
    chosen_login = st.selectbox("Select Access Identity Profile Node:", options=list(selector_map.keys()), format_func=lambda x: selector_map[x])
    
    if st.button("🔓 Authenticate & Mount Session", type="primary", use_container_width=True):
        st.session_state["active_iam_user"] = chosen_login
        st.session_state["iam_logged_in"] = True
        st.success(f"Session established for {st.session_state['iam_directory'][chosen_login]['name']}!")
        st.rerun()
    st.stop()

# ─── 🛡️ DYNAMIC ROLE-BASED ACCESS CONTROL TAB ROUTER ───
active_user_key = st.session_state["active_iam_user"]
user_profile = st.session_state["iam_directory"][active_user_key]
visible_tabs_list = user_profile["tabs"]

generated_tabs = st.tabs([f"🔒 {t}" if t != "IAM Security & Access Controls" else f"🔐 {t}" for t in visible_tabs_list])
tab_mapping = dict(zip(visible_tabs_list, generated_tabs))

from tabs import tab1_dashboard, tab2_gemma4, tab3_registry, tab4_reremediation, tab5_iam

if "Operational Dashboard" in tab_mapping:
    with tab_mapping["Operational Dashboard"]: tab1_dashboard.render(engine, min_threshold)
if "Conversational Gemma4" in tab_mapping:
    with tab_mapping["Conversational Gemma4"]: tab2_gemma4.render(engine, min_threshold)
if "Account Directory Lookup" in tab_mapping:
    with tab_mapping["Account Directory Lookup"]: tab3_registry.render(engine)
if "Remediation & Actions Console" in tab_mapping:
    with tab_mapping["Remediation & Actions Console"]: tab4_reremediation.render(engine)
if "IAM Security & Access Controls" in tab_mapping:
    with tab_mapping["IAM Security & Access Controls"]: tab5_iam.render(user_profile)
