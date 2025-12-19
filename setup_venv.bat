@echo off
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To use the script:
echo   1. Activate the venv: venv\Scripts\activate.bat
echo   2. Run the script: python search_and_open_pdfs.py
pause

