@echo off
title Servidor Minecraft 1.12.2
cd /d "%~dp0"
"%USERPROFILE%\curseforge\minecraft\Install\java\Jre_8\bin\java.exe" -Xms4G -Xmx6G -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M -jar forge-1.12.2-14.23.5.2860.jar nogui
pause
