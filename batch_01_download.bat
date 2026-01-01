@echo off
REM Download PDFs for Batch 1
echo ====================================================================
echo DOWNLOADING BATCH 1 PDFs
echo ====================================================================
echo.
echo Make sure you're on the first PDF tab in Chrome!
echo.

python download_batch.py batch_01

echo.
echo ====================================================================
echo Check: pdf\batch_01\
echo ====================================================================
echo.
pause
