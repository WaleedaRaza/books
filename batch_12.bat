@echo off
REM Batch 12 [EVEN]: Books 276-300
REM Source: Newbooks.txt (line-based)
echo ====================================================================
echo BATCH 12 [EVEN]: Books 276-300
echo ====================================================================
echo.
echo Run ODD batches (1,3,5,7...) on one machine
echo Run EVEN batches (2,4,6,8...) on another machine
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 276 300

echo.
echo ====================================================================
echo BATCH 12 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_12_download.bat
echo.
pause
