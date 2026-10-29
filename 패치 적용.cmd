@echo off
chcp 65001 >nul
if "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -File "%~dp0패치 선택.ps1"
) else (
  "%~dp0Cobra2PatchApplier.exe" %*
)
set "patch_result=%errorlevel%"
pause
exit /b %patch_result%
