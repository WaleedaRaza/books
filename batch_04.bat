@echo off
REM Batch 4: Books 76-100
echo ====================================================================
echo BATCH 4: Books 76-100
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 76 100

echo.
echo ====================================================================
echo BATCH 4 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_04_download.bat
echo.
pause
