@echo off
REM Batch 13: Books 301-325
echo ====================================================================
echo BATCH 13: Books 301-325
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 301 325

echo.
echo ====================================================================
echo BATCH 13 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_13_download.bat
echo.
pause
