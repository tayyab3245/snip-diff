# PyInstaller build script for NIP-Diff
# Build with:  pyinstaller -y pyinstaller.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    hiddenimports=['PySide6.QtSvg'],   # ensure Qt plugins are bundled
    datas=[('nip/assets/*', 'assets')],
    strip=False,
    upx=True
)

pyz  = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe  = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='nip-diff',
    console=False,      # windowed
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='nip-diff'
)
