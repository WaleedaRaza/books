@echo off
REM Batch 8: Books 176-200
echo ====================================================================
echo BATCH 8: Books 176-200
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 176 200

echo.
echo ====================================================================
echo BATCH 8 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_08_download.bat
echo.
pause
