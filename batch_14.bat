@echo off
REM Batch 14: Books 326-350
echo ====================================================================
echo BATCH 14: Books 326-350
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 326 350

echo.
echo ====================================================================
echo BATCH 14 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_14_download.bat
echo.
pause
