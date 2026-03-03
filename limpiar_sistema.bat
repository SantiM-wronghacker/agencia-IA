@echo off
REM Limpiar todos los procesos Python
echo Matando todos los procesos Python...
taskkill /F /IM python.exe 2>nul

REM Esperar a que se cierren
timeout /t 3 /nobreak

REM Liberar puertos
echo Liberando puertos 8000 y 8080...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 "') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080 "') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak

echo Sistema limpio. Puedes ejecutar arrancar.bat
pause
