@echo off
REM Batch 34: Books 826-850
echo ====================================================================
echo BATCH 34: Books 826-850
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 826 850

echo.
echo ====================================================================
echo BATCH 34 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_34_download.bat
echo.
pause
