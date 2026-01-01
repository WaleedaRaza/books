@echo off
REM Batch 6: Books 126-150
echo ====================================================================
echo BATCH 6: Books 126-150
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 126 150

echo.
echo ====================================================================
echo BATCH 6 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_06_download.bat
echo.
pause
