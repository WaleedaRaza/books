@echo off
REM Batch 26: Books 626-650
echo ====================================================================
echo BATCH 26: Books 626-650
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 626 650

echo.
echo ====================================================================
echo BATCH 26 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_26_download.bat
echo.
pause
