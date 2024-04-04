@echo off
start "" "C:\Program Files\Oray\SunLogin\SunloginClient\SunloginClient.exe"
start "" "C:\Program Files\Tailscale\tailscale-ipn.exe"

powershell -ExecutionPolicy Bypass -File ".\\sunshine.ps1"