# =====================================================================
# ─── RISK-GEMMA4-AGENT: AUTOMATED DATA SIMULATOR ENGINE (PART 1) ────
# ─── POPULATES CORE INTERACTIVE PROFILE MAPS & DECOUPLED SCHEMAS ─────
# =====================================================================
import os
import pandas as pd

def generate_production_sandbox_datasets():
    print("⏳ Initializing Standalone Sandbox Dataset Generator...")
    
    # Ensure target data subdirectory folder exists safely on the disk
    os.makedirs("data", exist_ok=True)
    
    # ─── PROFILE LOG DIRECTORY MATRIX (data/account_master.csv) ───
    accounts_data = [
        {
            "ACCOUNT_ID": "ACC_991", "CUSTOMER_NAME": "Alpha Global Holdings", "KYC_STATUS": "Pending", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": False, "PAN": "PAN-ALPH991A", "GSTIN": "27ALPHA9911B1ZS", 
            "IEC_CODE": "IEC_9910042401", "TRADE_LICENSE": "LIC_991_ALPHA_HOUSE", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "14, Nariman Point, Cuffe Parade, Mumbai",
            "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK", "OUTBOUND_OVERRIDE_ENABLED": "false", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_112", "CUSTOMER_NAME": "Rajesh Kumar", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Individual", "IS_PEP": False, "PAN": "PAN-RAJE112K", "GSTIN": "N/A", 
            "IEC_CODE": "N/A", "TRADE_LICENSE": "N/A", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "45, MG Road, Connaught Place, New Delhi",
            "SYSTEMIC_LOCK_STATUS": "UNLOCKED", "OUTBOUND_OVERRIDE_ENABLED": "true", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_445", "CUSTOMER_NAME": "Omega Trade Corp", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": False, "PAN": "PAN-OMEG445C", "GSTIN": "27OMEGA4452C1ZS", 
            "IEC_CODE": "IEC_4450098202", "TRADE_LICENSE": "LIC_445_OMEGA_CORP", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "88, IT Park, Electronic City, Bengaluru",
            "SYSTEMIC_LOCK_STATUS": "UNLOCKED", "OUTBOUND_OVERRIDE_ENABLED": "true", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_101", "CUSTOMER_NAME": "Srinivasta Enterprises", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": True, "PAN": "PAN-SRIN101E", "GSTIN": "27SRINI1013A1ZS", 
            "IEC_CODE": "IEC_1010077703", "TRADE_LICENSE": "LIC_101_SRINI_HOUSE", "CURRENT_BALANCE": 45750000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "12, MVP Colony, Visakhapatnam, Andhra Pradesh",
            "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK", "OUTBOUND_OVERRIDE_ENABLED": "false", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_202", "CUSTOMER_NAME": "Anita Sharma", "KYC_STATUS": "Pending", 
            "CUSTOMER_TYPE": "Individual", "IS_PEP": True, "PAN": "PAN-ANIT202S", "GSTIN": "N/A", 
            "IEC_CODE": "N/A", "TRADE_LICENSE": "N/A", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "72, Jubilee Hills, Road No 3, Hyderabad",
            "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK", "OUTBOUND_OVERRIDE_ENABLED": "false", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_303", "CUSTOMER_NAME": "Zeta Logistics", "KYC_STATUS": "Suspended", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": False, "PAN": "PAN-ZETA303L", "GSTIN": "27ZETAL3034D1ZS", 
            "IEC_CODE": "IEC_3030012104", "TRADE_LICENSE": "LIC_303_ZETA_LOGS", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "5, Salt Lake Sector V, Kolkata",
            "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK", "OUTBOUND_OVERRIDE_ENABLED": "false", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_505", "CUSTOMER_NAME": "Vikram Malhotra", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Individual", "IS_PEP": False, "PAN": "PAN-VIKR505M", "GSTIN": "N/A", 
            "IEC_CODE": "N/A", "TRADE_LICENSE": "N/A", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "104, Boat Club Road, Poona, Maharashtra",
            "SYSTEMIC_LOCK_STATUS": "UNLOCKED", "OUTBOUND_OVERRIDE_ENABLED": "true", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_606", "CUSTOMER_NAME": "Sigma Ventures", "KYC_STATUS": "Pending", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": False, "PAN": "PAN-SIGM606V", "GSTIN": "27SIGMA6065E1ZS", 
            "IEC_CODE": "IEC_6060033205", "TRADE_LICENSE": "LIC_606_SIGMA_VENT", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "31, Sector 17, Chandigarh, Punjab",
            "SYSTEMIC_LOCK_STATUS": "ACTIVE_LOCK", "OUTBOUND_OVERRIDE_ENABLED": "false", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_707", "CUSTOMER_NAME": "Priya Patel", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Individual", "IS_PEP": False, "PAN": "PAN-PRIY707P", "GSTIN": "N/A", 
            "IEC_CODE": "N/A", "TRADE_LICENSE": "N/A", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "19, GIDC Industrial Estate, Vadodara, Gujarat",
            "SYSTEMIC_LOCK_STATUS": "UNLOCKED", "OUTBOUND_OVERRIDE_ENABLED": "true", "COMPLIANCE_REMARKS": "NA"
        },
        {
            "ACCOUNT_ID": "ACC_808", "CUSTOMER_NAME": "Nexus Infotech", "KYC_STATUS": "Verified", 
            "CUSTOMER_TYPE": "Corporate", "IS_PEP": False, "PAN": "PAN-NEXU808I", "GSTIN": "27NEXUS8086F1ZS", 
            "IEC_CODE": "IEC_8080066106", "TRADE_LICENSE": "LIC_808_NEXUS_INFO", "CURRENT_BALANCE": 1250000, 
            "AD_BANK": "State Bank of India", "PERMANENT_ADDRESS": "61, JN Road, Alwarpet, Chennai, Tamil Nadu",
            "SYSTEMIC_LOCK_STATUS": "UNLOCKED", "OUTBOUND_OVERRIDE_ENABLED": "true", "COMPLIANCE_REMARKS": "NA"
        }
    ]
    pd.DataFrame(accounts_data).to_csv("data/account_master.csv", index=False)
    print("✅ Rebuilt account_master.csv cleanly with unified Snowflake schemas.")
    # =====================================================================
    # ─── RISK-GEMMA4-AGENT: AUTOMATED DATA SIMULATOR ENGINE (PART 2) ────
    # ─── POPULATES COMPREHENSIVE HISTORICAL RAW TRANSACTION HISTORIES ────
    # =====================================================================
    ledger_entries = [
        # 🚨 NEW VIOLATION TARGET VECTORS: Injected to fulfill Rule 1 (Sanctioned Countries Auto-Freeze)
        {"TRANSACTION_ID": "TX9001", "ACCOUNT_ID": "ACC_303", "AMOUNT": 520000, "COUNTRY_CODE": "KP", "TIMESTAMP": "2026-10-19 09:00:00"},
        {"TRANSACTION_ID": "TX9002", "ACCOUNT_ID": "ACC_606", "AMOUNT": 890000, "COUNTRY_CODE": "IR", "TIMESTAMP": "2026-10-19 09:15:00"},
        {"TRANSACTION_ID": "TX9003", "ACCOUNT_ID": "ACC_991", "AMOUNT": 145000, "COUNTRY_CODE": "MM", "TIMESTAMP": "2026-10-19 09:30:00"},
        {"TRANSACTION_ID": "TX9004", "ACCOUNT_ID": "ACC_112", "AMOUNT": 310000, "COUNTRY_CODE": "SY", "TIMESTAMP": "2026-10-19 10:10:00"},
        
        # 👥 ORIGINAL HISTORICAL ENTRIES: Completely retained without modification
        {"TRANSACTION_ID": "TX1001", "ACCOUNT_ID": "ACC_991", "AMOUNT": 7500000, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-15 14:22:00"},
        {"TRANSACTION_ID": "TX1002", "ACCOUNT_ID": "ACC_112", "AMOUNT": 120000, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-15 15:30:00"},
        {"TRANSACTION_ID": "TX1003", "ACCOUNT_ID": "ACC_991", "AMOUNT": 6200000, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-16 09:11:00"},
        {"TRANSACTION_ID": "TX1004", "ACCOUNT_ID": "ACC_445", "AMOUNT": 4500000, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-16 11:45:00"},
        {"TRANSACTION_ID": "TX1005", "ACCOUNT_ID": "ACC_112", "AMOUNT": 7556, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-16 13:07:00"},
        {"TRANSACTION_ID": "TX1006", "ACCOUNT_ID": "ACC_445", "AMOUNT": 1769583, "COUNTRY_CODE": "AE", "TIMESTAMP": "2026-09-16 13:25:00"},
        {"TRANSACTION_ID": "TX1007", "ACCOUNT_ID": "ACC_991", "AMOUNT": 1621945, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-16 15:58:00"},
        {"TRANSACTION_ID": "TX1008", "ACCOUNT_ID": "ACC_101", "AMOUNT": 9192600, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-16 18:02:00"},
        {"TRANSACTION_ID": "TX1009", "ACCOUNT_ID": "ACC_808", "AMOUNT": 4717265, "COUNTRY_CODE": "UK", "TIMESTAMP": "2026-09-16 20:00:00"},
        {"TRANSACTION_ID": "TX1010", "ACCOUNT_ID": "ACC_303", "AMOUNT": 4711907, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-16 20:36:00"},
        {"TRANSACTION_ID": "TX1011", "ACCOUNT_ID": "ACC_112", "AMOUNT": 100595, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-16 22:14:00"},
        {"TRANSACTION_ID": "TX1012", "ACCOUNT_ID": "ACC_808", "AMOUNT": 4487923, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-17 00:41:00"},
        {"TRANSACTION_ID": "TX1013", "ACCOUNT_ID": "ACC_112", "AMOUNT": 100230, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-17 03:31:00"},
        {"TRANSACTION_ID": "TX1014", "ACCOUNT_ID": "ACC_808", "AMOUNT": 6117228, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-17 03:58:00"},
        {"TRANSACTION_ID": "TX1015", "ACCOUNT_ID": "ACC_991", "AMOUNT": 3873498, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-17 04:33:00"},
        {"TRANSACTION_ID": "TX1016", "ACCOUNT_ID": "ACC_505", "AMOUNT": 73869, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-17 05:24:00"},
        {"TRANSACTION_ID": "TX1017", "ACCOUNT_ID": "ACC_303", "AMOUNT": 6010453, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-17 08:19:00"},
        {"TRANSACTION_ID": "TX1018", "ACCOUNT_ID": "ACC_112", "AMOUNT": 160680, "COUNTRY_CODE": "UK", "TIMESTAMP": "2026-09-17 10:45:00"},
        {"TRANSACTION_ID": "TX1019", "ACCOUNT_ID": "ACC_101", "AMOUNT": 2791438, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-17 13:38:00"},
        {"TRANSACTION_ID": "TX1020", "ACCOUNT_ID": "ACC_707", "AMOUNT": 58570, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-17 14:46:00"},
        {"TRANSACTION_ID": "TX1021", "ACCOUNT_ID": "ACC_991", "AMOUNT": 5342423, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-17 15:12:00"},
        {"TRANSACTION_ID": "TX1022", "ACCOUNT_ID": "ACC_101", "AMOUNT": 9565702, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-17 16:16:00"},
        {"TRANSACTION_ID": "TX1023", "ACCOUNT_ID": "ACC_606", "AMOUNT": 6687601, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-17 17:02:00"},
        {"TRANSACTION_ID": "TX1024", "ACCOUNT_ID": "ACC_202", "AMOUNT": 37603, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-17 19:41:00"},
        {"TRANSACTION_ID": "TX1025", "ACCOUNT_ID": "ACC_505", "AMOUNT": 153969, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-17 20:47:00"},
        {"TRANSACTION_ID": "TX1026", "ACCOUNT_ID": "ACC_445", "AMOUNT": 8598432, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-17 21:09:00"},
        {"TRANSACTION_ID": "TX1027", "ACCOUNT_ID": "ACC_112", "AMOUNT": 41066, "COUNTRY_CODE": "UK", "TIMESTAMP": "2026-09-17 23:07:00"},
        {"TRANSACTION_ID": "TX1028", "ACCOUNT_ID": "ACC_808", "AMOUNT": 1115818, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-18 01:32:00"},
        {"TRANSACTION_ID": "TX1029", "ACCOUNT_ID": "ACC_202", "AMOUNT": 146024, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-18 03:59:00"},
        {"TRANSACTION_ID": "TX1030", "ACCOUNT_ID": "ACC_202", "AMOUNT": 169024, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-18 05:24:00"},
        {"TRANSACTION_ID": "TX1031", "ACCOUNT_ID": "ACC_505", "AMOUNT": 42460, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-18 06:41:00"},
        {"TRANSACTION_ID": "TX1032", "ACCOUNT_ID": "ACC_707", "AMOUNT": 47832, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-18 09:31:00"},
        {"TRANSACTION_ID": "TX1033", "ACCOUNT_ID": "ACC_202", "AMOUNT": 168496, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-18 10:20:00"},
        {"TRANSACTION_ID": "TX1034", "ACCOUNT_ID": "ACC_303", "AMOUNT": 2760343, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-18 12:35:00"},
        {"TRANSACTION_ID": "TX1035", "ACCOUNT_ID": "ACC_991", "AMOUNT": 1926828, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-18 12:59:00"},
        {"TRANSACTION_ID": "TX1036", "ACCOUNT_ID": "ACC_101", "AMOUNT": 9568669, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-18 15:13:00"},
        {"TRANSACTION_ID": "TX1037", "ACCOUNT_ID": "ACC_112", "AMOUNT": 140645, "COUNTRY_CODE": "UK", "TIMESTAMP": "2026-09-18 18:11:00"},
        {"TRANSACTION_ID": "TX1038", "ACCOUNT_ID": "ACC_606", "AMOUNT": 9274173, "COUNTRY_CODE": "CH", "TIMESTAMP": "2026-09-18 20:36:00"},
        {"TRANSACTION_ID": "TX1039", "ACCOUNT_ID": "ACC_808", "AMOUNT": 7149076, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-18 22:05:00"},
        {"TRANSACTION_ID": "TX1040", "ACCOUNT_ID": "ACC_505", "AMOUNT": 177078, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-19 00:27:00"},
        {"TRANSACTION_ID": "TX1041", "ACCOUNT_ID": "ACC_606", "AMOUNT": 2080113, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-19 02:03:00"},
        {"TRANSACTION_ID": "TX1042", "ACCOUNT_ID": "ACC_991", "AMOUNT": 9920182, "COUNTRY_CODE": "KY", "TIMESTAMP": "2026-09-19 04:43:00"},
        {"TRANSACTION_ID": "TX1043", "ACCOUNT_ID": "ACC_101", "AMOUNT": 170642, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-19 05:51:00"},
        {"TRANSACTION_ID": "TX1044", "ACCOUNT_ID": "ACC_112", "AMOUNT": 9234, "COUNTRY_CODE": "US", "TIMESTAMP": "2026-09-19 08:12:00"},
        {"TRANSACTION_ID": "TX1045", "ACCOUNT_ID": "ACC_101", "AMOUNT": 4722073, "COUNTRY_CODE": "UK", "TIMESTAMP": "2026-09-19 10:48:00"},
        {"TRANSACTION_ID": "TX1046", "ACCOUNT_ID": "ACC_808", "AMOUNT": 7980103, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-19 12:42:00"},
        {"TRANSACTION_ID": "TX1047", "ACCOUNT_ID": "ACC_101", "AMOUNT": 1632524, "COUNTRY_CODE": "AE", "TIMESTAMP": "2026-09-19 14:22:00"},
        {"TRANSACTION_ID": "TX1048", "ACCOUNT_ID": "ACC_505", "AMOUNT": 108767, "COUNTRY_CODE": "IN", "TIMESTAMP": "2026-09-19 17:19:00"},
        {"TRANSACTION_ID": "TX1049", "ACCOUNT_ID": "ACC_112", "AMOUNT": 16889, "COUNTRY_CODE": "SG", "TIMESTAMP": "2026-09-19 17:56:00"},
        {"TRANSACTION_ID": "TX1050", "ACCOUNT_ID": "ACC_101", "AMOUNT": 3264348, "COUNTRY_CODE": "HK", "TIMESTAMP": "2026-09-19 18:41:00"}
    ]
    
    pd.DataFrame(ledger_entries).to_csv("data/transaction_ledger.csv", index=False)
    print("✅ Rebuilt transaction_ledger.csv natively with active core audit logs.")
    print("🏁 [SUCCESS] Standalone testing datasets are completely synchronized.")

if __name__ == "__main__":
    generate_production_sandbox_datasets()
