@echo off
REM Batch 15: Books 351-375
echo ====================================================================
echo BATCH 15: Books 351-375
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 351 375

echo.
echo ====================================================================
echo BATCH 15 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_15_download.bat
echo.
pause
