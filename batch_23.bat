@echo off
REM Batch 23: Books 551-575
echo ====================================================================
echo BATCH 23: Books 551-575
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 551 575

echo.
echo ====================================================================
echo BATCH 23 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_23_download.bat
echo.
pause
