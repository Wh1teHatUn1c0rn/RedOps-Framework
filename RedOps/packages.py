import os
import shutil
from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

# Define source and target paths
redops_src = project_root / "RedOps"
deb_root = project_root / "builds" / "redops_deb"
exe_root = project_root / "builds" / "redops_exe"

# Clean up and recreate DEB structure
(deb_root / "DEBIAN").mkdir(parents=True, exist_ok=True)
opt_redops_path = deb_root / "opt" / "redops"
shutil.copytree(redops_src, opt_redops_path, dirs_exist_ok=True)

# Write DEB control file
control_content = """
Package: redops
Version: 1.0
Section: pentest
Priority: optional
Architecture: all
Maintainer: OffensiveUn1cornCrew
Description: RedOps Recon Suite - Modular Red Teaming Toolkit
"""
control_file = deb_root / "DEBIAN" / "control"
control_file.write_text(control_content.strip() + "\n")

# Create EXE build structure
exe_redops_path = exe_root / "RedOps"
exe_redops_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(redops_src, exe_redops_path, dirs_exist_ok=True)

# Output
print(f"[*] DEB directory: {deb_root.resolve()}")
print(f"[*] EXE directory: {exe_root.resolve()}")

