@echo off
REM Batch 5: Books 101-125
echo ====================================================================
echo BATCH 5: Books 101-125
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 101 125

echo.
echo ====================================================================
echo BATCH 5 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_05_download.bat
echo.
pause
