@echo off
REM Batch 28: Books 676-700
echo ====================================================================
echo BATCH 28: Books 676-700
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 676 700

echo.
echo ====================================================================
echo BATCH 28 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_28_download.bat
echo.
pause
