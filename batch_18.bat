@echo off
REM Batch 18: Books 426-450
echo ====================================================================
echo BATCH 18: Books 426-450
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 426 450

echo.
echo ====================================================================
echo BATCH 18 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_18_download.bat
echo.
pause
