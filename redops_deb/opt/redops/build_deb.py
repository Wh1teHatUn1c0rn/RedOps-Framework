import os
import shutil
from pathlib import Path

print("[*] Setting up .deb packaging structure...")

# Define project root
project_root = Path(__file__).resolve().parents[0]
redops_source = project_root / "RedOps"
deb_root = project_root / "builds" / "deb"
deb_package_path = project_root / "builds" / "redops_1.0_all.deb"

if deb_root.exists():
    shutil.rmtree(deb_root)

(deb_root / "DEBIAN").mkdir(parents=True, exist_ok=True)
install_path = deb_root / "opt" / "redops"
install_path.mkdir(parents=True, exist_ok=True)

print("[*] Copying RedOps framework into /opt/redops...")
shutil.copytree(redops_source, install_path, dirs_exist_ok=True)

print("[*] Writing control file...")
control_content = """\
Package: redops
Version: 1.0
Section: pentest
Priority: optional
Architecture: all
Maintainer: OffensiveUn1cornCrew
Description: RedOps Recon Suite - Modular Red Teaming Toolkit
"""
control_file_path = deb_root / "DEBIAN" / "control"
control_file_path.write_text(control_content.strip() + "\n")

print("[*] Building .deb package...")
os.system(f"dpkg-deb --build {deb_root} {deb_package_path}")

print(f"[*] .deb package built successfully: {deb_package_path.resolve()}")