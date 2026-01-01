@echo off
REM Batch 22: Books 526-550
echo ====================================================================
echo BATCH 22: Books 526-550
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 526 550

echo.
echo ====================================================================
echo BATCH 22 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_22_download.bat
echo.
pause
