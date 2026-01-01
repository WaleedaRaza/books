@echo off
REM Batch 44: Books 1076-1100
echo ====================================================================
echo BATCH 44: Books 1076-1100
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1076 1100

echo.
echo ====================================================================
echo BATCH 44 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_44_download.bat
echo.
pause
