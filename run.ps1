Write-Host "=== Cyber-Groq-Ransomware ===" -ForegroundColor Cyan
if (-not (Test-Path .venv)) {
Write-Host "Creating virtual environment ..." -ForegroundColor Yellow
python -m venv .venv
}
..venv\Scripts\Activate.ps1
Write-Host "Installing/updating dependencies ..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null
Write-Host "Starting server ..." -ForegroundColor Green
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000