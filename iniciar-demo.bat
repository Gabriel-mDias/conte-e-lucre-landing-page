@echo off
title Iniciar Demonstracao Local — Sample Landing Page
echo ========================================================
echo   INICIANDO DEMONSTRACAO LOCAL (SAMPLE LANDING PAGE)
echo ========================================================
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado no sistema!
    echo Por favor, instale o Node.js em https://nodejs.org para prosseguir.
    pause
    exit /b 1
)

if not exist "node_modules\" (
    echo [1/3] Instalando dependencias do projeto (npm install)...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao instalar dependencias!
        pause
        exit /b 1
    )
) else (
    echo [1/3] Dependencias ja instaladas.
)

echo.
echo [2/3] Compilando versao otimizada (npm run build)...
call npm run build
if %errorlevel% neq 0 (
    echo [ERRO] Falha no build da pagina!
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando servidor local e abrindo navegador...
echo Pressione Ctrl+C nesta janela para encerrar o servidor.
echo.
call npx vite preview --open

pause