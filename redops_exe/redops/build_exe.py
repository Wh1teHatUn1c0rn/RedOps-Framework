import os
import shutil
from pathlib import Path

# Define base project root dynamically (script location)
project_root = Path(__file__).resolve().parents[0]

# Define build directory inside the project
exe_build_dir = project_root / "builds" / "exe_build"
exe_build_dir.mkdir(parents=True, exist_ok=True)

# Define source paths
source_main = project_root / "RedOps" / "redops.py"
source_core = project_root / "RedOps" / "core"

# Copy main script and core directory
shutil.copy(source_main, exe_build_dir)
shutil.copytree(source_core, exe_build_dir / "core", dirs_exist_ok=True)

# Generate PyInstaller .spec file
spec_file_path = exe_build_dir / "redops.spec"
spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['redops.py'],
    pathex=['.'],
    binaries=[],
    datas=[('core/*', 'core')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='redops',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='redops'
)
"""

with open(spec_file_path, "w") as f:
    f.write(spec_content.strip())

print(spec_file_path.resolve())

