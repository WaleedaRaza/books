@echo off
REM Batch 16: Books 376-400
echo ====================================================================
echo BATCH 16: Books 376-400
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 376 400

echo.
echo ====================================================================
echo BATCH 16 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_16_download.bat
echo.
pause
