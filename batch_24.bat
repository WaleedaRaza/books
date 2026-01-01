@echo off
REM Batch 24: Books 576-600
echo ====================================================================
echo BATCH 24: Books 576-600
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 576 600

echo.
echo ====================================================================
echo BATCH 24 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_24_download.bat
echo.
pause
