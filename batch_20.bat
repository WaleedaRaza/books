@echo off
REM Batch 20: Books 476-500
echo ====================================================================
echo BATCH 20: Books 476-500
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 476 500

echo.
echo ====================================================================
echo BATCH 20 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_20_download.bat
echo.
pause
