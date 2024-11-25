@echo off
echo "Waiting for rodnmod process to stop in order to proceed updating! Please do not close this window."
:check
tasklist /FI "IMAGENAME eq rodnmod.exe" 2>NUL | find /I "rodnmod.exe" > NUL
if errorlevel 1 (
    7zr x update.7z -y
    del update.7z
    .\rodnmod
) else (
    timeout /t 5 > NUL
    goto check
)