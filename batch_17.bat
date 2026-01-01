@echo off
REM Batch 17: Books 401-425
echo ====================================================================
echo BATCH 17: Books 401-425
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 401 425

echo.
echo ====================================================================
echo BATCH 17 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_17_download.bat
echo.
pause
