@echo off
REM Batch 38: Books 926-950
echo ====================================================================
echo BATCH 38: Books 926-950
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 926 950

echo.
echo ====================================================================
echo BATCH 38 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_38_download.bat
echo.
pause
