@echo off
REM Batch 37: Books 901-925
echo ====================================================================
echo BATCH 37: Books 901-925
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 901 925

echo.
echo ====================================================================
echo BATCH 37 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_37_download.bat
echo.
pause
