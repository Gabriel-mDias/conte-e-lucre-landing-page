@echo off
title Publicar Demonstracao no GitHub Pages
echo ========================================================
echo   PUBLICAR DEMONSTRACAO NO GITHUB PAGES
echo ========================================================
echo.

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado no sistema!
    pause
    exit /b 1
)

echo [1/3] Validando build local antes de publicar...
call npm run build
if %errorlevel% neq 0 (
    echo [ERRO] O build falhou! Corrija os erros antes de publicar.
    pause
    exit /b 1
)

echo.
echo [2/3] Enviando alteracoes para o GitHub...
git add .
set /p COMMIT_MSG="Digite uma descricao para a atualizacao (ou pressione Enter para padrao): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=feat: atualizar demonstracao da landing page

git commit -m "%COMMIT_MSG%"
git push origin HEAD

echo.
echo [3/3] Publicacao disparada com sucesso!
echo O GitHub Actions iniciou a publicacao automatica.
echo Acesse o seu repositorio no GitHub > Actions para acompanhar o deploy no GitHub Pages.
echo.
pause