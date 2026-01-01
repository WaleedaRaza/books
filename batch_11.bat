@echo off
REM Batch 11: Books 251-275
echo ====================================================================
echo BATCH 11: Books 251-275
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 251 275

echo.
echo ====================================================================
echo BATCH 11 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_11_download.bat
echo.
pause
