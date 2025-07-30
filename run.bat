@echo off
echo === Cyber-Groq-Ransomware ===
if not exist .venv\ (
echo Creating virtual environment ...
python -m venv .venv
)
call .venv\Scripts\activate.bat
echo Installing/updating dependencies ...
pip install -r requirements.txt >nul
echo Starting server ...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000