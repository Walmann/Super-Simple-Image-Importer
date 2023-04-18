import sys
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {
#     "includes": [],
#     "excludes": ["tkinter", "unittest"],
#     # "zip_include_packages": [],
# }
# bdist_msi_options = {
#     "data": {
#         "initial_target_dir": "[ProgramFiles64Folder]SSII",
#         "directory_table": [
#             ("ProgramMenuFolder", "TARGETDIR", "."),
#             ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
#         ],
#         "ProgId": [
#             ("Prog.Id", None, None, "This is a description", "IconId", None),
#         ],
#         "Icon": [
#             ("IconId", "Assets/icon.png"),
#         ],
#         "includefiles": ['mainWindow.ui', "Assets/icon.png"],
#     },
# }

executables = [
    Executable(
        "importer.py",
        # copyright="Copyright (C) 2023 cx_Freeze",
        base="Win32GUI" if sys.platform == "win32" else None,
        icon="Assets/icon.png",
        shortcut_name="Super Simple Image Importer",
        shortcut_dir="MyProgramMenu",
    ),
]

# TODO CONT This script does not work. I just need make it install a working copy. App icons and everything else can wait.


# base="Win32GUI" should be used only for Windows GUI app
# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="SSII (Super Simple Image Importer)",
    version="0.1",
    description="Super simple image importer!",
    executables=executables,
    options={
        "build_exe":
            {   
                "includes": ["PyQt5.QtWidgets", "PyQt5.QtGui", "PyQt5.uic", "PyQt5.QtCore", ],
                "include_files": ["mainWindow.ui"],
                "excludes": ["tkinter", "unittest"],
                # "zip_include_packages": [],
            },
        "bdist_msi":
        {
            "data":
                {
                    "initial_target_dir": "[ProgramFiles64Folder]SSII",
                    "directory_table": [
                        ("ProgramMenuFolder", "TARGETDIR", "."),
                        ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
                    ],
                    "ProgId": [
                        ("Prog.Id", None, None, "This is a description", "IconId", None),
                    ],
                    "Icon": [
                        ("IconId", "Assets/icon.png"),
                    ],
                    "includefiles": ['mainWindow.ui', "Assets/icon.png"],
                }
            }
    }
)
