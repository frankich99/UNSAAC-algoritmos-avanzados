@echo off
cd /d "%~dp0"
echo =================================================================
echo Subiendo proyecto a GitHub (UNSAAC - Algoritmos Avanzados)
echo =================================================================
echo.
git push origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo [EXITO] Todo el proyecto fue subido correctamente a GitHub.
) else (
    echo [AVISO] Ocurrio un problema al conectar con GitHub. Revisa tus credenciales.
)
echo.
pause
