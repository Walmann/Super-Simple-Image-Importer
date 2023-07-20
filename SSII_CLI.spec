# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:\\WORKFOLDER\\Super_Simple_Image_Importer/src/app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\WORKFOLDER\\Super_Simple_Image_Importer/src/Assets', 'Assets/'), ('C:\\WORKFOLDER\\Super_Simple_Image_Importer/src/ui', 'ui/'), ('C:\\WORKFOLDER\\Super_Simple_Image_Importer/src/bin', 'bin/')],
    hiddenimports=['PySide6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SSII_CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='Installer\\version_info.txt',
    icon=['C:\\WORKFOLDER\\Super_Simple_Image_Importer\\src\\Assets\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SSII_CLI',
)
