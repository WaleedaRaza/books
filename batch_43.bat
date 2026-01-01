@echo off
REM Batch 43: Books 1051-1075
echo ====================================================================
echo BATCH 43: Books 1051-1075
echo ====================================================================
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 1051 1075

echo.
echo ====================================================================
echo BATCH 43 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_43_download.bat
echo.
pause
