@echo off
REM Download PDFs for Batch 42
echo ====================================================================
echo DOWNLOADING BATCH 42 PDFs
echo ====================================================================
echo.
echo Make sure you're on the first PDF tab in Chrome!
echo.

python download_batch.py batch_42

echo.
echo ====================================================================
echo Check: pdf\batch_42\
echo ====================================================================
echo.
pause
