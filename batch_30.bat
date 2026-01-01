@echo off
REM Batch 30: Books 726-750
echo ====================================================================
echo BATCH 30: Books 726-750
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 726 750

echo.
echo ====================================================================
echo BATCH 30 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_30_download.bat
echo.
pause
