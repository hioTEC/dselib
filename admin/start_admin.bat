@echo off
chcp 65001 > nul
setlocal
echo ========================================
echo   DSE Library Admin Starter
echo ========================================
echo.

echo [1/2] Start backend API...
start "DSELib Backend" cmd /k "cd /d %~dp0 && python admin_server.py"

%SystemRoot%\System32\timeout.exe /t 2 /nobreak > nul

echo [2/2] Start admin frontend...
start "DSELib Admin Frontend" cmd /k "cd /d %~dp0 && python -m http.server -d .. 5173"

echo.
echo Services started:
echo   API:   http://127.0.0.1:8088
echo   Admin: http://localhost:5173/admin/admin.html
echo.
echo Press any key to open admin UI...
pause > nul

start http://localhost:5173/admin/admin.html
endlocal
