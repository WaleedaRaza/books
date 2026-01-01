@echo off
REM Batch 25: Books 601-625
echo ====================================================================
echo BATCH 25: Books 601-625
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 601 625

echo.
echo ====================================================================
echo BATCH 25 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_25_download.bat
echo.
pause
