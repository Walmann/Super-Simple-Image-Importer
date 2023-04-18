; Define the name of the installer
Name "Super Simple Image Importer"

; Define the output file
OutFile "SuperSimpleImageImporterInstaller.exe"

; Set the installation directory
InstallDir $PROGRAMFILES\SuperSimpleImageImporter

; Start the default section
Section

  ; Set the output path for files
  SetOutPath $INSTDIR

  ; Add files to the installer
  File "Importer.exe"
  File "dialogRenameFile.ui"
  File "mainWindow.ui"

  ; Create a shortcut on the desktop
  CreateShortcut "$DESKTOP\Super Simple Image Importer.lnk" "$INSTDIR\Importer.exe" "" "$INSTDIR\Assets\icon.ico"

  ; Create a shortcut in the start menu
  CreateDirectory "$SMPROGRAMS\Super Simple Image Importer"
  CreateShortcut "$SMPROGRAMS\Super Simple Image Importer\Super Simple Image Importer.lnk" "$INSTDIR\Importer.exe" "" "$INSTDIR\Assets\icon.ico"

; End the default section
SectionEnd