@echo off
REM Batch 21: Books 501-525
echo ====================================================================
echo BATCH 21: Books 501-525
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 501 525

echo.
echo ====================================================================
echo BATCH 21 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_21_download.bat
echo.
pause
