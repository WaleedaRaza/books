@echo off
REM Batch 1: Books 1-25
echo ====================================================================
echo BATCH 1: Books 1-25
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1 25

echo.
echo ====================================================================
echo BATCH 1 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_01_download.bat
echo.
pause
