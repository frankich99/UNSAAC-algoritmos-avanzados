@echo off
chcp 65001 > nul
title UNSAAC - Algoritmos Avanzados - Laboratorio 01 (Grupo 5)
echo ===============================================================================
echo  EJECUCION AUTOMATIZADA - LABORATORIO 01: COMPLEJIDAD Y EXPERIMENTACION
echo  GRUPO 5 - ALGORITMOS AVANZADOS (UNSAAC)
echo ===============================================================================
echo.
echo Verificando entorno de Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se encontro Python en el PATH del sistema.
    echo Asegurese de tener Python 3.10 o superior instalado.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Ejecutando todos los algoritmos y generando graficos/datos (Modo 100%% Offline)...
python ejecutar_todo.py

echo.
echo ===============================================================================
echo  PROCESO COMPLETADO
echo  Revise los archivos PNG generados y el documento INFORME_Y_GUIA_EJECUCION.md
echo ===============================================================================
pause
