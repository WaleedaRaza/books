@echo off
REM Batch 10: Books 226-250
echo ====================================================================
echo BATCH 10: Books 226-250
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 226 250

echo.
echo ====================================================================
echo BATCH 10 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_10_download.bat
echo.
pause
