@echo off
cd /d "%~dp0"
start "SMARTFLOW Backend" cmd /k "cd /d %~dp0\backend && python -m uvicorn app.main:app --reload"
start "SMARTFLOW Frontend" cmd /k "cd /d %~dp0 && streamlit run frontend\app.py"
