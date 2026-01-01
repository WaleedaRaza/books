@echo off
REM Batch 29: Books 701-725
echo ====================================================================
echo BATCH 29: Books 701-725
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 701 725

echo.
echo ====================================================================
echo BATCH 29 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_29_download.bat
echo.
pause
