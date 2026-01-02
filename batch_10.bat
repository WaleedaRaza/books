@echo off
REM Batch 10 [EVEN]: Books 226-250
REM Source: Newbooks.txt (line-based)
echo ====================================================================
echo BATCH 10 [EVEN]: Books 226-250
echo ====================================================================
echo.
echo Run ODD batches (1,3,5,7...) on one machine
echo Run EVEN batches (2,4,6,8...) on another machine
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range 226 250

echo.
echo ====================================================================
echo BATCH 10 SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: batch_10_download.bat
echo.
pause
