@echo off
REM Batch 54: Books 1326-1326
echo ====================================================================
echo BATCH 54: Books 1326-1326
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1326 1326

echo.
echo ====================================================================
echo BATCH 54 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_54_download.bat
echo.
pause
