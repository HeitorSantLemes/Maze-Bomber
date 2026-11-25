@echo off
title Maze Bomber
cd /d "%~dp0"
if not exist .venv (
    echo Criando o ambiente virtual pela primeira vez...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Instalando as dependencias do jogo...
    pip install pygame-ce
) else (
    call .venv\Scripts\activate.bat
)
python main.py
pause