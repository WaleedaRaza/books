@echo off
REM Batch 40: Books 976-1000
echo ====================================================================
echo BATCH 40: Books 976-1000
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 976 1000

echo.
echo ====================================================================
echo BATCH 40 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_40_download.bat
echo.
pause
