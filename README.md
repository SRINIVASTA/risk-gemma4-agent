# 🛡️ Risk-Gemma4-Agent Panel

An enterprise-grade **Anti-Money Laundering (AML) and Counter-Terrorist Financing (CFT)** risk intelligence dashboard panel. This system couples high-performance automated data processing with deep semantic compliance reasoning via the **Gemma 4 LLM** architecture (`gemma-4-26b-a4b-it`) and **LangChain Vector RAG stores**, adhering strictly to the Reserve Bank of India (RBI) Master KYC Directions.

## 🏗️ System Architecture & Line-of-Custody

The platform is engineered using a modular, decoupled architecture separating stateless analytical data compute layers (`gemma4_engine.py`) from dynamic, role-restricted presentation layers (`app.py` and `tabs/`). 

```mermaid
graph TD
    A[Structured Data: Ledger Logs] -->|Pandas Ingest| B(gemma4_engine.py Core)
    A2[policies/rbi_aml_directions.txt] -->|FAISS Vector Store| B
    
    subgraph Stateless Reasoning Engine
        B --> C{Signal Detection}
        C -->|Section 4.1 / 4.2 Breaks| D[Enhanced Risk Vector]
        C -->|Section 7.3 Layering| E[48hr Rolling Windows]
        C -->|Section 9.4 Mule Checks| F[Micro-Velocity Alerts]
    end
    
    B -->|Stateless Payload Query| G[Gemma 4 Model Client Inference]
    G -->|Raw Text Report Output| H[tabs/ presentation layers]
    
    subgraph Dynamic State UI Shell
        H --> I[tab1_dashboard: Read-Only Matrix Render]
        H --> J[tab4_reremediation: State Write Controls]
    end
    
    J -->|Mutates session_state Sign-Off| I
```

---

## 🔀 Compliance Pipeline Execution Sequence

The terminal operates on a strict three-step line-of-custody pipeline tracking financial anomalies from signal detection to audit-ready legal documentation:

```mermaid
sequenceDiagram
    autonumber
    actor Officer as Compliance Officer (Tab 1)
    participant Engine as gemma4_engine.py
    participant VDB as FAISS Vector Store (RBI Base)
    participant G4 as Gemma 4 AI Instance (Google SDK)
    participant UI_T4 as Remediation Desk (Tab 4)

    Officer->>Engine: Trigger "Run Global Compliance Audit Pipeline"
    Note over Engine: Normalizes Data & Evaluates Sections 4.1, 4.2, 7.3, 9.4
    Engine->>Engine: Run 48hr Cross-Border Rolling Window Vector Math
    Engine-->>Officer: Step 1 Complete: Output signals_df Dataframe Matrix & Plots
    
    Engine->>VDB: Similarity Search Vector Query (FATF, PEP, Mule profiles)
    VDB-->>Engine: Recover Exact Regulation Chunk Snippets
    Engine-->>Officer: Step 2 Complete: Output raw evidence_cleaned Text Stream
    
    Engine->>G4: Generate Content Payload Request (Stateless Variables + Context)
    Note over G4: Model-Level Deep Deep Reasoning Suite Executing...
    G4-->>Engine: Return Structured markdown Compliance Breach Breakdown
    
    UI_T4->>Officer: Fetch Live State Token (st.session_state.report_review_status)
    Note over Officer: Presentation layer compiles text report layout + Live Signature Footer
    Engine-->>Officer: Step 3 Complete: Render Final Report & Build ReportLab PDF Binary
```

---

## 🔐 Identity & Access Management (IAM) Matrix

The system simulates a zero-trust financial backoffice terminal with rigid **Role-Based Access Control (RBAC)** filters managed from a centralized sidebar login terminal.

| Identity Profile Registry | Access Role Node | Clearance Hierarchy | Unlocked Workspace Channels | Write Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **Appala Srinivas Tanakala** | `SYSTEM_ADMIN` | Level 4 - Full Access | All 5 Application Tabs | Full provisioning, system parameters configuration, manual overrides, cache clearance. |
| **Anita Sharma** | `COMPLIANCE_ANALYST` | Level 2 - Intelligence Access | Tabs 1, 2, 3, 4 | Dispatch targeted locks, execute remediation holds, converse with Gemma4 Core. |
| **Priya Patel** | `SENIOR_AUDITOR` | Level 3 - Audit Review | Tabs 1, 3, 5 (**Read-Only**) | Read data logs, extract ReportLab PDF packages. Tab 5 user-creation is **hidden and write-locked**. |
| **Rajesh Kumar** | `JUNIOR_CLERK` | Level 1 - Basic Read | Tab 1 Only | Read-only access to main dashboard KPIs. All other panels hidden. |

---

## ⚙️ Automated Compliance Core Engine Rules

1. **Section 4.1 High-Value Cross-Border Rule:** Flags cross-border moves exceeding ₹5,000,000 to FATF tax havens (`KY`, `CH`). If marked `IS_PEP`, prompts for senior verification.
2. **Section 4.2 Unverified PEP Lockout:** If an outbound transaction is initiated by a `Pending` KYC account flagged as a Politically Exposed Person (`IS_PEP == True`), the engine overrides standard risk formulas and throws an **Immediate 100% Risk Score System Lock**.
3. **Section 7.3 Layering Velocity Math:** Groups corporate ledgers dynamically to catch entities executing separate international transaction legs to multiple offshore country codes within a rolling 48-hour window (+25 Risk Index Multiplier).
4. **Section 9.4 Cyber-Fraud Mule Sweep:** Scans small-scale routing logs down to **₹1,000** on unverified or suspended account nodes to identify micro-smurfing networks, triggering an automated placeholder in the `REMEDIATION_LOG`.

---

## 🛠️ Repository File Subdirectory Tree

```text
risk-gemma4-agent/
├── app.py                  # Orchestrator core hub, memory registers, global sidebar session controller
├── gemma4_engine.py        # Stateless backend analytical compute, math vectors, similarity searches
├── requirements.txt        # System application dependency pinning configuration
├── data/
│   ├── account_master.csv       # Centralized consumer profiles and KYC verification metadata
│   └── transaction_ledger.csv   # Financial transaction ledger payload logs
├── policies/
│   └── rbi_aml_directions.txt   # Official regulatory policy text used for similarity context injection
└── tabs/
    ├── __init__.py         # Module package indicator file (Ensures clean cross-imports)
    ├── tab1_dashboard.py   # Run compliance audits, view Plotly graphs, export ReportLab PDFs
    ├── tab2_gemma4.py      # Conversational Gemma4 compliance assistant workspace
    ├── tab3_registry.py    # Customer 360 lookup, tracks active locks, blocks ledger access on active freezes
    ├── tab4_reremediation.py# Dispatch manual containment protocols, run automated rules loops
    └── tab5_iam.py         # IAM security simulation desk (Features write-lock overrides for Auditors)
```

---

## 🚀 Quick Start Deployment Guide

### 1. Provision Local Virtual Environment Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Workspace Keys
```bash
export GOOGLE_API_KEY="your-gemini-api-key-from-google-ai-studio"
```

### 3. Launch the Streamlit Terminal Instance
```bash
streamlit run app.py
```
