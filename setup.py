from cx_Freeze import setup, Executable
import sys

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
