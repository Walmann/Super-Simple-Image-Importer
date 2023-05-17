@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "GithubURL=https://api.github.com/repos/Walmann/SuperSimpleImageImporter/releases/latest"
set "InstallLocation=%LOCALAPPDATA%\Programs\Super Simple Image Importer"

set "TempZipFile=%TEMP%\temp.zip"

echo Laster ned zipfil fra %GithubURL%...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%GithubURL%', '%TempZipFile%')"
echo Zipfil lastet ned.

echo Pakker ut zipfil til %InstallLocation%...
powershell -Command "Expand-Archive -Path '%TempZipFile%' -DestinationPath '%InstallLocation%' -Force"
echo Zipfil pakket ut.

echo Starter programmet...
cd /d "%InstallLocation%"
start "" "start.exe"

endlocal