@echo off
REM Batch 33: Books 801-825
echo ====================================================================
echo BATCH 33: Books 801-825
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 801 825

echo.
echo ====================================================================
echo BATCH 33 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_33_download.bat
echo.
pause
