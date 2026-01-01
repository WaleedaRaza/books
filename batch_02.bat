@echo off
REM Batch 2: Books 26-50
echo ====================================================================
echo BATCH 2: Books 26-50
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 26 50

echo.
echo ====================================================================
echo BATCH 2 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_02_download.bat
echo.
pause
