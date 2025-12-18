@echo off
chcp 65001 > nul
setlocal
echo ========================================
echo   DSE Library Website Starter
echo ========================================
echo.
echo Serving frontend at http://localhost:8000/
echo.
start "" cmd /k "cd /d %~dp0 && python -m http.server -d ..\frontend 8000"
echo Press any key to open the site...
pause > nul
start http://localhost:8000/
endlocal
