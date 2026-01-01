@echo off
REM Batch 52: Books 1276-1300
echo ====================================================================
echo BATCH 52: Books 1276-1300
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1276 1300

echo.
echo ====================================================================
echo BATCH 52 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_52_download.bat
echo.
pause
