@echo off
REM Batch 31 [ODD]: Books 751-775
REM Source: Newbooks.txt (line-based)
echo ====================================================================
echo BATCH 31 [ODD]: Books 751-775
echo ====================================================================
echo.
echo Run ODD batches (1,3,5,7...) on one machine
echo Run EVEN batches (2,4,6,8...) on another machine
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
