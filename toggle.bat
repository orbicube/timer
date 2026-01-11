@echo off
if exist %~dp0\run (
	del %~dp0\run
) else (
	copy NUL %~dp0\run
)