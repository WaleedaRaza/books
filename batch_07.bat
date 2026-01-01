@echo off
REM Batch 7: Books 151-175
echo ====================================================================
echo BATCH 7: Books 151-175
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 151 175

echo.
echo ====================================================================
echo BATCH 7 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_07_download.bat
echo.
pause
