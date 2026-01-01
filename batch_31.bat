@echo off
REM Batch 31: Books 751-775
echo ====================================================================
echo BATCH 31: Books 751-775
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 751 775

echo.
echo ====================================================================
echo BATCH 31 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_31_download.bat
echo.
pause
