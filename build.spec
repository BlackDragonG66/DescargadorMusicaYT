# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file para Descargador de Música de YouTube

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['yt_dlp', 'pygame', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DescargadorMusicaYT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
