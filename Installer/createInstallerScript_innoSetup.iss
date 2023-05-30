
[Setup]
AppName=Super Simple Image Importer
AppVersion=V0.1
WizardStyle=modern
DefaultDirName={autopf}\SSII
DefaultGroupName=Super Simple Image Importer
UninstallDisplayIcon={app}\SSII.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Setup_Build
OutputBaseFilename=SuperSimpleImageImporterSetup



[Files]
Source: "Exe_Dest\SSII\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Opprett en snarvei på skrivebordet"; GroupDescription: "Snarveier:";
Name: "startmenuicon"; Description: "Opprett en snarvei i startmenyen"; GroupDescription: "Snarveier:";
;Name: "quicklaunchicon"; Description: "Opprett en snarvei i oppgavelinjen"; GroupDescription: "Snarveier:"; OnlyBelowVersion: 6.1
Name: "startafterinstall"; Description: "Kjør programmet etter installasjonen"; GroupDescription: "Etter installasjon:";

[Icons]
Name: "{group}\Super Simple Image Importer"; Filename: "{app}\SSII.exe"
Name: "{userdesktop}\Super Simple Image Importer"; Filename: "{app}\SSII.exe"; Tasks: desktopicon
Name: "{userstartmenu}\Super Simple Image Importer"; Filename: "{app}\SSII.exe"; Tasks: startmenuicon
;Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\SSII"; Filename: "{app}\SSII.exe"; Tasks: quicklaunchicon; OnlyBelowVersion: 6.1

[Run]
Filename: "{app}\SSII.exe"; Description: "{cm:LaunchProgram,SSII}"; Flags: nowait postinstall skipifsilent; Tasks: startafterinstall