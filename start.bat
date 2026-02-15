@echo off
cd /d "%~dp0"
pip install requests -q 2>nul
python api_tester.py
pause
