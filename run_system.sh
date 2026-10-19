#!/bin/bash
echo "====================================================================="
echo "🛡️ RISK-GEMMA4-AGENT: CORE INITIALIZATION SEQUENCE (SRINIVASTA)"
echo "====================================================================="
echo ""
echo "⏳ Step 1: Running Sandbox Data Simulator Engine..."
python3 generate_mock_data.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Data generation failed. Check your Python installation."
    exit 1
fi
echo ""
echo "⏳ Step 2: Wiping Old Local CSV Log Cache..."
rm -f data/remediation_log.csv
echo ""
echo "⏳ Step 3: Launching Streamlit Risk Dashboard UI Console..."
python3 -m streamlit run app.py
