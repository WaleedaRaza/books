@echo off
REM Batch 53: Books 1301-1325
echo ====================================================================
echo BATCH 53: Books 1301-1325
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1301 1325

echo.
echo ====================================================================
echo BATCH 53 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_53_download.bat
echo.
pause
