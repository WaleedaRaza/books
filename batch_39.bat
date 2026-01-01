@echo off
REM Batch 39: Books 951-975
echo ====================================================================
echo BATCH 39: Books 951-975
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 951 975

echo.
echo ====================================================================
echo BATCH 39 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_39_download.bat
echo.
pause
