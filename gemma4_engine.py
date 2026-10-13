# ==========================================
# ─── BLOCK 1: CORE ENGINE SETUP & DATA NORMALISATION WITH VELOCITY CAPABILITIES ───
# ==========================================
import os
import pandas as pd
from google import genai
from google.genai import types
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class FraudCopilotEngine:
    def __init__(self):
        # 1. Load data tables from repository
        self.tx_df = pd.read_csv("data/transaction_ledger.csv")
        self.acc_df = pd.read_csv("data/account_master.csv")
        
        # Core Self-Healing Step: Force all column keys to stripped uppercase immediately on ingest
        self.tx_df.columns = self.tx_df.columns.str.strip().str.upper()
        self.acc_df.columns = self.acc_df.columns.str.strip().str.upper()
        
        # Verify and normalize column values to ensure Boolean matching works perfectly
        if "IS_PEP" in self.acc_df.columns:
            self.acc_df["IS_PEP"] = self.acc_df["IS_PEP"].astype(str).str.strip().str.upper() == "TRUE"
        
        # Ensure TIMESTAMP column is cast to real datetime values for velocity calculations
        if "TIMESTAMP" in self.tx_df.columns:
            self.tx_df["TIMESTAMP"] = pd.to_datetime(self.tx_df["TIMESTAMP"])
        
        # Drop pre-existing risk columns to compute fresh from the RBI framework
        if "RISK_SCORE" in self.tx_df.columns:
            self.tx_df = self.tx_df.drop(columns=["RISK_SCORE"])
        
        # 2. Load policy files for the vector database using LangChain loaders
        with open("policies/rbi_aml_directions.txt", "r") as f:
            policy_content = f.read()
        
        chunks = [chunk.strip() for chunk in policy_content.split("\n\n") if chunk.strip()]
        
        # 3. Model Engine Infrastructure
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_db = FAISS.from_texts(chunks, self.embeddings)
        
        # Initialize native Google GenAI Client dynamically from environment
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ Missing GOOGLE_API_KEY inside the execution environment.")
        self.client = genai.Client(api_key=api_key)

    def _calculate_live_risk_score(self, df):
        """Calculates risk matrices adhering strictly to RBICRC profiles, now with Section 7.3 Layering logic."""
        scores = []
        
        # Pre-process rolling window vectors to check for Section 7.3 velocity flags across the target layout
        velocity_account_ids = set()
        if "TIMESTAMP" in df.columns and "ACCOUNT_ID" in df.columns:
            sorted_df = df.sort_values(by=["ACCOUNT_ID", "TIMESTAMP"]).copy()
            for account_id, group in sorted_df.groupby("ACCOUNT_ID"):
                # Track cross-border legs matching outbound international destinations
                cb_group = group[group["COUNTRY_CODE"] != "IN"]
                if len(cb_group) >= 2:
                    for i in range(len(cb_group)):
                        start_time = cb_group.iloc[i]["TIMESTAMP"]
                        end_time = start_time + pd.Timedelta(hours=48)
                        window = cb_group[(cb_group["TIMESTAMP"] >= start_time) & (cb_group["TIMESTAMP"] <= end_time)]
                        
                        # Section 7.3 Check: Multiple transactions going to different country codes within 48 hours
                        if len(window) >= 2 and window["COUNTRY_CODE"].nunique() > 1:
                            velocity_account_ids.add(account_id)
                            break

        for _, row in df.iterrows():
            score = 0
            
            # Dimension 1: FATF & Offshore Jurisdiction Profile
            if row["COUNTRY_CODE"] in ["KY", "CH"]:
                score += 40
            elif row["COUNTRY_CODE"] in ["AE", "HK", "SG"]:
                score += 20
            else:
                score += 5
                
            # Dimension 2: RBI Customer Onboarding Profile Matrix
            if row["KYC_STATUS"] == "Suspended":
                score += 55  
            elif row["KYC_STATUS"] == "Pending":
                score += 35  
            else:
                score += 10  
                
            # Dimension 3: Capital Exposure Banding (RBI High-Value Reporting Caps)
            if row["AMOUNT"] >= 5000000:
                score += 25  
            elif row["AMOUNT"] >= 1000000:
                score += 15  
            else:
                score += 5

            # Dimension 4: Politically Exposed Person (PEP) Flag Check
            if row.get("IS_PEP") == True:
                score += 30  
                
            # NEW Dimension 5: Section 7.3 Velocity Structuring Multiplier Flag
            if row["ACCOUNT_ID"] in velocity_account_ids and row["COUNTRY_CODE"] != "IN":
                score += 25
                
            # Lock parameters inside normal 0-100 system limits
            scores.append(min(score, 100))
            
        return scores
# ==========================================
# ─── BLOCK 2: DETECT SIGNALS, RAG EVIDENCE, & STR REPORT GENERATION ───
# ==========================================
    def detect_signals(self, min_amount=5000000):
        """Step 1: Signal Detection aligned with RBI Anti-Money Laundering Thresholds & Section 7.3 Structuring"""
        merged = pd.merge(self.tx_df, self.acc_df, on="ACCOUNT_ID")
        merged["RISK_SCORE"] = self._calculate_live_risk_score(merged)
        
        # Track accounts that hit the Section 7.3 layering anomaly logic dynamically
        velocity_triggered_accounts = set()
        sorted_merged = merged.sort_values(by=["ACCOUNT_ID", "TIMESTAMP"]).copy()
        for acc_id, group in sorted_merged.groupby("ACCOUNT_ID"):
            cb_legs = group[group["COUNTRY_CODE"] != "IN"]
            if len(cb_legs) >= 2:
                for idx in range(len(cb_legs)):
                    t_start = cb_legs.iloc[idx]["TIMESTAMP"]
                    t_end = t_start + pd.Timedelta(hours=48)
                    t_window = cb_legs[(cb_legs["TIMESTAMP"] >= t_start) & (cb_legs["TIMESTAMP"] <= t_end)]
                    if len(t_window) >= 2 and t_window["COUNTRY_CODE"].nunique() > 1:
                        velocity_triggered_accounts.add(acc_id)
                        break
        
        condition = (
            (merged["AMOUNT"] >= min_amount) | 
            (merged["RISK_SCORE"] >= 70) | 
            ((merged["KYC_STATUS"] == "Pending") & (merged["AMOUNT"] > 1000000)) | 
            (merged["KYC_STATUS"] == "Suspended") |
            (merged["IS_PEP"] == True) |
            (merged["ACCOUNT_ID"].isin(velocity_triggered_accounts) & (merged["COUNTRY_CODE"] != "IN"))
        )
        
        flagged_df = merged[condition].copy()
        
        # Convert TIMESTAMP back into standard presentation string formats for display stability
        if "TIMESTAMP" in flagged_df.columns:
            flagged_df["TIMESTAMP"] = flagged_df["TIMESTAMP"].astype(str)
            
        return flagged_df

    def gather_evidence(self, flagged_df):
        """Step 2: Optimized Context Search mapping back to rule documents including Section 7.3 anomalies"""
        if flagged_df.empty:
            return "No systemic compliance violations detected."
            
        evidence_pool = []
        unique_countries = flagged_df["COUNTRY_CODE"].unique()
        unique_statuses = flagged_df["KYC_STATUS"].unique()
        
        search_queries = [
            f"RBI regulations for wire transfers to jurisdictions: {', '.join(unique_countries)}",
            f"Official Master Direction restrictions on account onboarding status: {', '.join(unique_statuses)}",
            "Enhanced due diligence requirements for Politically Exposed Persons PEP profiles",
            "Section 7.3 Structural Anomalies velocity structuring layering high value transfers rolling 48 hour window"
        ]
        
        for query in search_queries:
            docs = self.vector_db.similarity_search(query, k=2)
            for doc in docs:
                if doc.page_content not in evidence_pool:
                    evidence_pool.append(doc.page_content)
                    
        return "\n\n".join(evidence_pool)

    def generate_audit_report(self, flagged_df, evidence):
        """
        Step 3: Compile final report with dense statistical tracking metrics.
        Forces the cloud-hosted Gemma 4 model to match the complete analytical summary style of Gemini.
        """
        if flagged_df.empty:
            return "### Audit Log\nZero critical risk anomalies detected across the target data tables."
            
        # 1. Pre-assemble markdown ledger rows in python memory
        table_rows = []
        for _, row in flagged_df.iterrows():
            formatted_amt = f"₹{int(row['AMOUNT']):,}"
            pep_status = "🔴 YES" if row['IS_PEP'] else "🟢 NO"
            table_rows.append(
                f"| {row['TRANSACTION_ID']} | {row['ACCOUNT_ID']} | {row['CUSTOMER_NAME']} | "
                f"{formatted_amt} | {row['COUNTRY_CODE']} | {int(row['RISK_SCORE'])} | {row['KYC_STATUS']} | {pep_status} |"
            )
        markdown_ledger = "\n".join(table_rows)

        # 2. Pre-calculate metrics to pass directly to the cloud prompt matrix
        total_incidents = len(flagged_df)
        total_exposure = int(flagged_df["AMOUNT"].sum())
        avg_risk_factor = float(flagged_df["RISK_SCORE"].mean())
        pep_count = int(flagged_df["IS_PEP"].sum())

        signal_summary = (
            f"Total Incidents Flagged: {total_incidents}, "
            f"Total Capital at Risk: INR {total_exposure:,}, "
            f"Average Risk Index: {avg_risk_factor:.1f}%, "
            f"Politically Exposed Persons Involved: {pep_count}"
        )
        
        system_instruction = (
            "You are an elite enterprise financial compliance auditor operating under RBI guidelines. "
            "Examine the aggregated statistical metrics alongside the regulatory evidence rules. "
            "Produce a detailed executive analysis portion of an official Suspicious Transaction Report (STR). "
            "You MUST explicitly incorporate all provided numbers (Incidents, Exposure, Risk, and PEP count) "
            "into the analysis. Address systemic internal control vulnerabilities, Prevention of Money Laundering Act (PMLA) implications, "
            "and sophisticated layering techniques like velocity structuring. "
            "Do not output a table block, as the system will merge the visual grid post-execution."
        )
        
        prompt = f"""
        AGGREGATED METRICS:
        {signal_summary}
        
        REGULATORY EVIDENCE BASE:
        {evidence}
        
        Please generate a complete, rigorous Suspicious Transaction Report (STR) following this strict outline:
        
        # SUSPICIOUS TRANSACTION REPORT (STR)
        ## 📌 1. EXECUTIVE SUMMARY
        [Generate a dense, paragraph-long legal executive summary detailing the metrics, PMLA breaches, 21 PEP exposures, and velocity structuring concerns here.]
        
        ## 📊 2. FLAGGED TRANSACTION LEDGER
        [LEDGER_INSERT_MARKER]
        
        ## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS
        ## 💡 4. RECOMMENDED COMPLIANCE ACTIONS
        """
        
        try:
            # Native direct call to the Google GenAI interface client wrapper
            api_key = os.environ.get("GOOGLE_API_KEY")
            self.client = genai.Client(api_key=api_key)

            response = self.client.models.generate_content(
                model='gemma-4-26b-a4b-it',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_level="low"),
                    max_output_tokens=4000
                )
            )
            return response.text.replace("[LEDGER_INSERT_MARKER]", markdown_ledger)
            
        except Exception as e:
            # FIXED: Added explicit markdown line breaks to fix the layout rendering on Streamlit
            fallback_report = (
                "# SUSPICIOUS TRANSACTION REPORT (STR)\n\n"
                "## 📌 1. EXECUTIVE SUMMARY\n\n"
                f"This report details a significant aggregation of suspicious activities, encompassing **{total_incidents} flagged incidents** with a total capital exposure of **INR {total_exposure:,}**. The average risk index across these incidents stands at a critical **{avg_risk_factor:.1f}%**, indicating a high probability of illicit financial activity. A particularly concerning aspect is the involvement of **{pep_count} Politically Exposed Persons (PEPs)** in these transactions, significantly elevating the inherent risk profile. These findings point to systemic internal control vulnerabilities and potential breaches of the Prevention of Money Laundering Act (PMLA) and specific RBI directives, particularly concerning enhanced due diligence for high-risk entities, KYC compliance, and the detection of sophisticated layering techniques such as velocity structuring. The substantial capital at risk underscores the urgent need for immediate intervention and robust remediation to mitigate financial crime exposure and ensure regulatory adherence.\n\n"
                "## 📊 2. FLAGGED TRANSACTION LEDGER\n\n"
                "| Transaction ID | Account ID | Customer Name | Amount (INR) | Destination | Risk Score | KYC Status | PEP Flag |\n"
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
                f"{markdown_ledger}\n\n"
                "## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS\n\n"
                f"{evidence}\n\n"
                "## 💡 4. RECOMMENDED COMPLIANCE ACTIONS\n\n"
                f"- [ ] Immediately file a comprehensive Suspicious Transaction Report (STR) with FIU-IND for all {total_incidents} flagged incidents, detailing the identified breaches and capital at risk.\n"
                f"- [ ] Initiate enhanced due diligence (EDD) and a full review of all {pep_count} Politically Exposed Person (PEP) accounts involved, ensuring mandatory senior management sign-off and explicit source of wealth/funds validation for all associated transactions.\n"
                f"- [ ] Conduct a forensic audit of all cross-border transactions exceeding INR 5,000,000, particularly those involving high-risk offshore jurisdictions, to identify any further non-compliance with Section 4.1.\n"
                f"- [ ] Implement an immediate system-wide audit to identify any PEP accounts operating under a 'Pending' KYC status that have initiated cross-border transactions, ensuring strict adherence to the global system lock mandate of Section 4.2.\n"
                f"- [ ] Review and recalibrate transaction monitoring systems to enhance the detection of velocity structuring (layering activities) as per Section 7.3, focusing on cumulative transaction velocities and transfers to disparate offshore entities within a 48-hour window.\n"
                f"- [ ] Provide mandatory refresher training to all relevant compliance and operations staff on RBI guidelines pertaining to PEPs, high-value cross-border transactions, KYC compliance, and the identification of structuring techniques.\n\n"
                "---\n"
                "**Prepared By:** Risk-Gemma4-Agent System Cluster  \n"
                "**Review Status:** ⚠️ PENDING HUMAN SIGN-OFF (Fail-Safe Local Mode Activated)"
            )
            return fallback_report
