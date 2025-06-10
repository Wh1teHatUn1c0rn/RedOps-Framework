import os
import shutil
import zipfile
from pathlib import Path

# Base project directory (adjust if needed)
project_root = Path(__file__).resolve().parents[0]

# Define dynamic paths
base_dir = project_root / "RedOps"
usb_dir = project_root / "USB_RedOps"
payloads_dir = usb_dir / "payloads"
dist_dir = project_root / "dist"
redops_exe_path = dist_dir / "redops.exe"
encrypted_zip_path = project_root / "redops_encrypted.zip"

# Create USB structure
if usb_dir.exists():
    shutil.rmtree(usb_dir)
usb_dir.mkdir(parents=True)
payloads_dir.mkdir(parents=True)

# Create autorun.inf
autorun_content = """[Autorun]
label=RedOps Toolkit
icon=redops.ico
open=redops.exe
"""
(usb_dir / "autorun.inf").write_text(autorun_content)

# Simulate payloads
(payloads_dir / "shellcode.bin").write_text("FAKE_SHELLCODE")
(payloads_dir / "redops.db").write_text("FAKE_DB")

# Copy redops.exe to USB root
shutil.copy2(redops_exe_path, usb_dir / "redops.exe")

# Create ZIP (note: Python's zipfile does not support encryption natively)
with zipfile.ZipFile(encrypted_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(base_dir)
            zipf.write(file_path, arcname)

# Final output paths
print(f"USB prepared at: {usb_dir}")
print(f"RedOps zip created at: {encrypted_zip_path}")