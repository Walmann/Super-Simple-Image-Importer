from cx_Freeze import setup, Executable
import sys


def create_zip():
    import os
    import zipfile
    import glob
    # Find the path to the MSI file in the ./dist directory
    msi_path = os.path.join("dist", "*.msi")
    msi_files = glob.glob(msi_path)
    if not msi_files:
        raise FileNotFoundError("No MSI files found in ./dist")
    msi_file = msi_files[0]

    # Search for a folder containing Importer.exe
    start_dir = "."
    importer_dir = None
    for dirpath, dirnames, filenames in os.walk(start_dir):
        if "Importer.exe" in filenames:
            importer_dir = dirpath
            break
    if importer_dir is None:
        raise FileNotFoundError("Could not find the Importer.exe folder")

    # Create the ZIP file with the same name as the MSI file
    zip_filename = os.path.splitext(msi_file)[0] + ".zip"
    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Add all files in the Importer.exe folder to the ZIP file
        for dirpath, dirnames, filenames in os.walk(importer_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                zf.write(filepath, arcname=os.path.relpath(filepath, start=importer_dir))
    print(f"Created {zip_filename}")
    exit()

import sys
if len(sys.argv) > 1 and sys.argv[1] == "create_zip":
    create_zip()



shortcut_table = [
    ('DesktopShortcut',        # Shortcut
     'DesktopFolder',          # Directory_
     'Super Simple Image Importer',  # Name
     'TARGETDIR',              # Component_
     '[TARGETDIR]Importer.exe',  # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,      # Icon path
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),
    ('StartMenuShortcut',      # Shortcut
     'StartMenuFolder',        # Directory_
     'Super Simple Image Importer',  # Name
     'TARGETDIR',                       # Component_
     '[TARGETDIR]Importer.exe',     # Target
     None,                          # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,      # Icon path
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
]



base = None

if sys.platform == 'win32':
    base = 'Win32GUI'


setup(
    name='Super Simple Image Importer',
    version='0.1',
    description='Super Simple Image Importer',
    executables=[
        Executable(
            'Importer.py',
            base=base,
            icon="./Assets/icon.ico",
        )
    ],
    options={
        'build_exe': {
            'include_files': ['dialogRenameFile.ui', 'mainWindow.ui', './Assets/icon.ico'],
            'packages': ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.uic"],
            # "includes": ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.uic"]
            'excludes': ["tkinter", "PyQt6", "unittest"],
            "optimize": 2
        },
        'bdist_msi': {
            'data': {
                'Shortcut': shortcut_table
            }
        }
    }
)



