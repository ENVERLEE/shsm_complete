# client.spec
# -*- mode: python ; coding: utf-8 -*-

# Get all required modules for client
client_hidden_imports = [
    'customtkinter',
    'tkinter',
    'PIL',
    'requests',
    'numpy',
    'pandas',
    'matplotlib',
] + collect_submodules('app.ui')

# Collect data files for client
client_datas = [
    ('app/ui/assets', 'app/ui/assets'),
    ('.env', '.'),
]

client_a = Analysis(
    ['app/ui/main_window.py'],  # Client entry point
    pathex=[],
    binaries=[],
    datas=client_datas,
    hiddenimports=client_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

client_pyz = PYZ(
    client_a.pure,
    client_a.zipped_data,
    cipher=block_cipher
)

client_exe = EXE(
    client_pyz,
    client_a.scripts,
    client_a.binaries,
    client_a.zipfiles,
    client_a.datas,
    [],
    name='Research-Client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI client doesn't need console
    icon='app/ui/assets/icon.icns',
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)