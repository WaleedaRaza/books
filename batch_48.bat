@echo off
REM Batch 48: Books 1176-1200
echo ====================================================================
echo BATCH 48: Books 1176-1200
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1176 1200

echo.
echo ====================================================================
echo BATCH 48 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_48_download.bat
echo.
pause
