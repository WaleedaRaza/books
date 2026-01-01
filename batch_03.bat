@echo off
REM Batch 3: Books 51-75
echo ====================================================================
echo BATCH 3: Books 51-75
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 51 75

echo.
echo ====================================================================
echo BATCH 3 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_03_download.bat
echo.
pause
