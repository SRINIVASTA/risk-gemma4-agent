@echo off
echo =====================================================================
echo 🛡️ RISK-GEMMA4-AGENT: CORE INITIALIZATION SEQUENCE (SRINIVASTA)
echo =====================================================================
echo.
echo ⏳ Step 1: Running Sandbox Data Simulator Engine...
python generate_mock_data.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Data generation failed. Check your Python installation.
    pause
    exit /b %errorlevel%
)
echo.
echo ⏳ Step 2: Wiping Old Local CSV Log Cache...
if exist data\remediation_log.csv del /f /q data\remediation_log.csv
echo.
echo ⏳ Step 3: Launching Streamlit Risk Dashboard UI Console...
python -m streamlit run app.py
pause
