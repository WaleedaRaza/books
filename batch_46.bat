@echo off
REM Batch 46: Books 1126-1150
echo ====================================================================
echo BATCH 46: Books 1126-1150
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1126 1150

echo.
echo ====================================================================
echo BATCH 46 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_46_download.bat
echo.
pause
