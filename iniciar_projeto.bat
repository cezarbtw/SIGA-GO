@echo off
title SIGA-GO | Sistema de Gestao Ambiental
echo ===================================================
echo      INICIANDO O SISTEMA SIGA-GO (ISO 14000)
echo ===================================================
echo.
echo 1. Iniciando o servidor backend FastAPI...
cd /d "%~dp0backend"
start "" "%~dp0backend\venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
timeout /t 2 >nul

echo 2. Abrindo o frontend no navegador padrao...
start "" "%~dp0frontend\index.html"

echo.
echo ===================================================
echo [OK] Backend rodando em: http://127.0.0.1:8000/docs
echo [OK] Frontend aberto com sucesso!
echo ===================================================
