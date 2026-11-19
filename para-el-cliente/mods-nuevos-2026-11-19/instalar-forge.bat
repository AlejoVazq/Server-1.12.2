@echo off
cd /d "%~dp0"
set "JAVA8=%USERPROFILE%\curseforge\minecraft\Install\java\Jre_8\bin\javaw.exe"
if not exist "%JAVA8%" (
  echo No se encontro el Java 8 de CurseForge en:
  echo %JAVA8%
  echo Instala Java 8 o abri el instalador con el.
  pause
  exit /b 1
)
start "" "%JAVA8%" -jar "forge-1.12.2-14.23.5.2860-installer.jar"
