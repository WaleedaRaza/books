@echo off
REM Batch 32: Books 776-800
echo ====================================================================
echo BATCH 32: Books 776-800
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 776 800

echo.
echo ====================================================================
echo BATCH 32 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_32_download.bat
echo.
pause
