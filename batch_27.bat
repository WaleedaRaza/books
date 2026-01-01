@echo off
REM Batch 27: Books 651-675
echo ====================================================================
echo BATCH 27: Books 651-675
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 651 675

echo.
echo ====================================================================
echo BATCH 27 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_27_download.bat
echo.
pause
