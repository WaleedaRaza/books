@echo off
REM Batch 50: Books 1226-1250
echo ====================================================================
echo BATCH 50: Books 1226-1250
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1226 1250

echo.
echo ====================================================================
echo BATCH 50 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_50_download.bat
echo.
pause
