@echo off
REM Batch 49: Books 1201-1225
echo ====================================================================
echo BATCH 49: Books 1201-1225
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1201 1225

echo.
echo ====================================================================
echo BATCH 49 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_49_download.bat
echo.
pause
