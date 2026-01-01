@echo off
REM Batch 9: Books 201-225
echo ====================================================================
echo BATCH 9: Books 201-225
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 201 225

echo.
echo ====================================================================
echo BATCH 9 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_09_download.bat
echo.
pause
