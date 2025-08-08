# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['.'],  # Add project root directory
    binaries=[],
    datas=[],
    hiddenimports=[
        'nip',
        'nip.ui',
        'nip.ui.file_tree',
        'nip.ui.enhanced_preview_panel', 
        'nip.ui.toolbar_neumorphic',
        'nip.ui.status_overlay',
        'nip.ui.neumorphic_scrollbar',
        'nip.ui.title_bar',
        'nip.ui.glass_window',
        'nip.ui.neumorphism',
        'nip.core',
        'nip.core.worker',
        'nip.core.fast_diff_worker',
        'nip.core.cached_diff_engine',
        'nip.core.diff_engine',
        'nip.core.snapshot',
        'nip.config',
        'nip.config.theme',
        'nip.config.defaults',
        'nip.config.tokens',
        'nip.config.dark_theme_new',
        'nip.config.light_theme_fixed',
        'shiboken6',
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SNIP-Diff',         # Set the final executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,           # CRITICAL: This hides the console window
    windowed=True,           # Use this as an alternative to console=False
    icon='icon.ico',         # CRITICAL: Add this line to include your icon
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
