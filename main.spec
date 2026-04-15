# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('./ui/qss/*.qss', './ui/qss'),
            ('./_internal/resources/imgs/*.png', './resources/imgs'),
            ('./_internal/resources/icons/*.png', './resources/icons'),
            ('./_internal/resources/icons/*.ico', './resources/icons'),
            ('./_internal/resources/icons/logo.ico', '.'),
            ('./_internal/resources/bin/*.exe','./resources/bin'),
            ('./_internal/resources/translations/*.qm','./resources/translations'),
            ('./_internal/manual','./manual')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = ('_internal/resources/icons/logo.ico')
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)