from pathlib import Path
import shutil

# Determine project root
try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

# Define paths
shell_script_path = project_root / "RedOps" / "redops_shell" / "shell.py"
deb_shell_dest = project_root / "builds" / "redops_deb" / "opt" / "redops" / "redops_shell" / "shell.py"
exe_shell_dest = project_root / "builds" / "redops_exe" / "RedOps" / "redops_shell" / "shell.py"

# Ensure destination directories exist
deb_shell_dest.parent.mkdir(parents=True, exist_ok=True)
exe_shell_dest.parent.mkdir(parents=True, exist_ok=True)

# Copy the shell script
shutil.copy2(shell_script_path, deb_shell_dest)
shutil.copy2(shell_script_path, exe_shell_dest)

# Confirm success
print(f"[*] Copied to DEB: {deb_shell_dest}")
print(f"[*] Copied to EXE: {exe_shell_dest}")

