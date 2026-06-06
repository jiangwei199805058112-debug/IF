@echo off
chcp 65001 > nul
set PYTHONUTF8=1
python -m if_game.main
pause
