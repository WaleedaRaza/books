@echo off
REM Batch 19: Books 451-475
echo ====================================================================
echo BATCH 19: Books 451-475
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 451 475

echo.
echo ====================================================================
echo BATCH 19 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_19_download.bat
echo.
pause
