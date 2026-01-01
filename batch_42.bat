@echo off
REM Batch 42: Books 1026-1050
echo ====================================================================
echo BATCH 42: Books 1026-1050
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1026 1050

echo.
echo ====================================================================
echo BATCH 42 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_42_download.bat
echo.
pause
