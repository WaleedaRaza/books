Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "`nActivating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "`nInstalling required packages..." -ForegroundColor Green
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nTo use the script:" -ForegroundColor Yellow
Write-Host "  1. Activate the venv: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "  2. Run the script: python search_and_open_pdfs.py" -ForegroundColor Cyan

