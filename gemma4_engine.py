import os
import pandas as pd
from google import genai
from google.genai import types
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class FraudCopilotEngine:
    def __init__(self):
        self.tx_df = pd.read_csv("data/transaction_ledger.csv")
        self.acc_df = pd.read_csv("data/account_master.csv")
        
        self.tx_df.columns = self.tx_df.columns.str.strip().str.upper()
        self.acc_df.columns = self.acc_df.columns.str.strip().str.upper()
        
        if "IS_PEP" in self.acc_df.columns:
            self.acc_df["IS_PEP"] = self.acc_df["IS_PEP"].astype(str).str.strip().str.upper() == "TRUE"
        
        if "TIMESTAMP" in self.tx_df.columns:
            self.tx_df["TIMESTAMP"] = pd.to_datetime(self.tx_df["TIMESTAMP"])
        
        if "RISK_SCORE" in self.tx_df.columns:
            self.tx_df = self.tx_df.drop(columns=["RISK_SCORE"])
            
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ Missing GOOGLE_API_KEY inside the execution environment.")
        self.client = genai.Client(api_key=api_key)
        
        with open("policies/rbi_aml_directions.txt", "r") as f:
            policy_content = f.read()
        
        chunks = [chunk.strip() for chunk in policy_content.split("\n\n") if chunk.strip()]
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)
        self.vector_db = FAISS.from_texts(chunks, self.embeddings)

    def _calculate_live_risk_score(self, df):
        scores = []
        velocity_account_ids = set()
        if "TIMESTAMP" in df.columns and "ACCOUNT_ID" in df.columns:
            sorted_df = df.sort_values(by=["ACCOUNT_ID", "TIMESTAMP"]).copy()
            for account_id, group in sorted_df.groupby("ACCOUNT_ID"):
                cb_group = group[group["COUNTRY_CODE"] != "IN"]
                if len(cb_group) >= 2:
                    for i in range(len(cb_group)):
                        start_time = cb_group.iloc[i]["TIMESTAMP"]
                        end_time = start_time + pd.Timedelta(hours=48)
                        window = cb_group[(cb_group["TIMESTAMP"] >= start_time) & (cb_group["TIMESTAMP"] <= end_time)]
                        if len(window) >= 2 and window["COUNTRY_CODE"].nunique() > 1:
                            velocity_account_ids.add(account_id)
                            break

        for _, row in df.iterrows():
            if row.get("IS_PEP") == True and row["KYC_STATUS"] == "Pending" and row["COUNTRY_CODE"] != "IN":
                scores.append(100)
                continue
                
            score = 0
            if row["COUNTRY_CODE"] in ["KY", "CH"]: score += 40
            elif row["COUNTRY_CODE"] in ["AE", "HK", "SG"]: score += 20
            else: score += 5
                
            if row["KYC_STATUS"] == "Suspended": score += 55  
            elif row["KYC_STATUS"] == "Pending": score += 35  
            else: score += 10  
                
            if row["AMOUNT"] >= 5000000: score += 25  
            elif row["AMOUNT"] >= 1000000: score += 15  
            else: score += 5

            if row.get("IS_PEP") == True: score += 30  
            if row["ACCOUNT_ID"] in velocity_account_ids and row["COUNTRY_CODE"] != "IN": score += 25
                
            scores.append(min(score, 100))
        return scores

    def detect_signals(self, min_amount=5000000):
        merged = pd.merge(self.tx_df, self.acc_df, on="ACCOUNT_ID")
        merged["RISK_SCORE"] = self._calculate_live_risk_score(merged)
        
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
            (merged["ACCOUNT_ID"].isin(velocity_triggered_accounts) & (merged["COUNTRY_CODE"] != "IN")) |
            ((merged["AMOUNT"] >= 1000) & (merged["KYC_STATUS"].isin(["Pending", "Suspended"])))
        )
        flagged_df = merged[condition].copy()
        if "TIMESTAMP" in flagged_df.columns:
            flagged_df["TIMESTAMP"] = flagged_df["TIMESTAMP"].astype(str)
        return flagged_df

    def gather_evidence(self, flagged_df):
        if flagged_df.empty: return "No systemic compliance violations detected."
        evidence_pool = []
        unique_countries = flagged_df["COUNTRY_CODE"].unique()
        unique_statuses = flagged_df["KYC_STATUS"].unique()
        
        search_queries = [
            f"RBI regulations for wire transfers to jurisdictions: {', '.join(unique_countries)}",
            f"Official Master Direction restrictions on account onboarding status: {', '.join(unique_statuses)}",
            "Enhanced due diligence requirements for Politically Exposed Persons PEP profiles",
            "Section 7.3 Structural Anomalies velocity structuring layering high value transfers rolling 48 hour window",
            "Section 9.4 Standard Operating Procedure for Suspected Money Mule Accounts"
        ]
        for query in search_queries:
            docs = self.vector_db.similarity_search(query, k=2)
            for doc in docs:
                if doc.page_content not in evidence_pool:
                    evidence_pool.append(doc.page_content)
        return "\n\n".join(evidence_pool)

    def generate_audit_report(self, flagged_df, evidence):
        if flagged_df.empty: return "### Audit Log\nZero critical risk anomalies detected across target data tables."
        table_rows = []
        for _, row in flagged_df.iterrows():
            formatted_amt = f"₹{int(row['AMOUNT']):,}"
            pep_status = "🔴 YES" if row['IS_PEP'] else "🟢 NO"
            table_rows.append(f"| {row['TRANSACTION_ID']} | {row['ACCOUNT_ID']} | {row['CUSTOMER_NAME']} | {formatted_amt} | {row['COUNTRY_CODE']} | {int(row['RISK_SCORE'])} | {row['KYC_STATUS']} | {pep_status} |")
        markdown_ledger = "\n".join(table_rows)

        total_incidents = len(flagged_df)
        total_exposure = int(flagged_df["AMOUNT"].sum())
        avg_risk_factor = float(flagged_df["RISK_SCORE"].mean())
        pep_count = int(flagged_df["IS_PEP"].sum())

        system_instruction = "You are an elite enterprise financial compliance auditor operating under RBI guidelines. Isolate broken sections. Format rules into structured markdown blocks with headings: 'Specific Section Broken:' and 'Evidence:'."
        prompt = f"REGULATORY EVIDENCE BASE:\n{evidence}\nExtract broken rules exactly: Specific Section Broken: [Name]\nEvidence: [Quote]"
        
        try:
            import streamlit as st
            active_tier_str = str(st.session_state.get("active_thinking_level", "MINIMAL")).upper()
            response = self.client.models.generate_content(
                model='gemma-4-26b-a4b-it',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction, temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_level=active_tier_str), max_output_tokens=3000
                )
            )
            ai_analysis_text = response.text if response.text else "Material infractions detected against regulatory boundaries."
            return f"# SUSPICIOUS TRANSACTION REPORT (STR)\n\n## 📌 1. EXECUTIVE SUMMARY\n\nThis report details a significant aggregation of suspicious activities, encompassing **{total_incidents} flagged incidents** with a total capital exposure of **INR {total_exposure:,}**. The average risk index stands at **{avg_risk_factor:.1f}%**.\n\n## 📊 2. FLAGGED TRANSACTION LEDGER\n\n| Transaction ID | Account ID | Customer Name | Amount (INR) | Destination | Risk Score | KYC Status | PEP Flag |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n{markdown_ledger}\n\n## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS\n\n{ai_analysis_text}\n\n## 💡 4. RECOMMENDED COMPLIANCE ACTIONS\n\n- [ ] Execute targeted temporary debit holds for Section 9.4 flagged mule accounts (max 60 days).\n- [ ] Initiate 20-day notification resolution window for justification documents.\n- [ ] Enforce immediate global system lock on any pending PEP profiles executing cross-border transfers.\n\n---\n**Prepared By:** Risk-Gemma4-Agent System Cluster  \n**Review Status:** {st.session_state.get('report_review_status', '⚠️ PENDING HUMAN SIGN-OFF')}"
        except Exception as e:
            return f"❌ Native Engine Extraction Drop: {str(e)}"
