@echo off
REM Script para compilar el ejecutable localmente

echo =================================================
echo Descargador de Musica de YouTube - Build Script
echo =================================================
echo.

echo Verificando si PyInstaller esta instalado...
.venv\Scripts\pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    .venv\Scripts\pip install pyinstaller
)

echo.
echo Compilando aplicacion...
.venv\Scripts\pyinstaller build.spec --noconfirm

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo compilar la aplicacion
    pause
    exit /b 1
)

echo.
echo =================================================
echo Compilacion completada exitosamente!
echo =================================================
echo.
echo El ejecutable se encuentra en:
echo   dist\DescargadorMusicaYT.exe
echo.
echo Para crear un release en GitHub:
echo   1. git tag -a v1.0.0 -m "Release v1.0.0"
echo   2. git push origin v1.0.0
echo.
pause
