# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files


a = Analysis(
    ['/Users/dimitarbakardzhiev/git/kedegit/kedehub/__main__.py'],
    pathex=['./venv311/lib/python3.11/site-packages/'],
    binaries=[],
    datas=collect_data_files('mmap'),  # This will include all necessary data files from mmap
    hiddenimports=['unidiff', 'git', 'gitdb', 'mmap', 'smmap', 'multiprocessing'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['test'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='kedegit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
