@echo off

call %~dp0venv\Scripts\activate

set TOKEN='paste token of your bot here'

python service_bot.py

pause