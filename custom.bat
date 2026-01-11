@echo off
set /p minutes=Minutes to add: 
set /a seconds=%minutes%*60
@echo %seconds% > %~dp0\custom