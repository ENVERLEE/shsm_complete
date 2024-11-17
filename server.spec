# server.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Get all required modules for server
server_hidden_imports = [
    'uvicorn',
    'fastapi',
    'sqlalchemy',
    'pydantic',
    'anthropic',
    'voyageai',
    'transformers',
    'numpy',
    'pandas',
    'alembic',
    'email_validator',
    'passlib',
    'python-jose',
    'databases',
    'argon2-cffi',
    'python-multipart',
] + collect_submodules('app')

# Collect data files for server
server_datas = [
    ('.env', '.'),
    ('alembic.ini', '.'),
    ('research.db', '.'),
] + collect_data_files('transformers')

server_a = Analysis(
    ['app/main.py'],  # Server entry point
    pathex=[],
    binaries=[],
    datas=server_datas,
    hiddenimports=server_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

server_pyz = PYZ(
    server_a.pure,
    server_a.zipped_data,
    cipher=block_cipher
)

server_exe = EXE(
    server_pyz,
    server_a.scripts,
    server_a.binaries,
    server_a.zipfiles,
    server_a.datas,
    [],
    name='Research-Server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Server needs console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

