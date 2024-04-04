@echo off
taskkill /f /im steam.exe
taskkill /f /im SteamService.exe

REG ADD HKEY_CURRENT_USER\SOFTWARE\Valve\Steam /v AutoLoginUser /t REG_SZ /d %1 /f

start "" "D:\Program Files (x86)\Steam\Steam.exe"

call "game.bat"
