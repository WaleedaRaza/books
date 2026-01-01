@echo off
REM Batch 41: Books 1001-1025
echo ====================================================================
echo BATCH 41: Books 1001-1025
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1001 1025

echo.
echo ====================================================================
echo BATCH 41 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_41_download.bat
echo.
pause
