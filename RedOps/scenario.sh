import os
import shutil
from pathlib import Path

try:
    project_root=Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

redops_dir = project_root / "RedOps"
scenario_path = redops_dir / "red_team_scenario.sh"
zip_path = project_root / "builds" / "RedOps_Framework.zip"

# Ensure builds directory exists
zip_path.parent.mkdir(parents=True, exist_ok=True)

scenario_script = """
#!/bin/bash

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: ./red_team_scenario.sh <target>"
    exit 1
fi

echo "[*] Running full RedOps red team scenario on $TARGET..."

# Activate Python virtual environment if exists
if [ -f redops_env/bin/activate ]; then
    source redops_env/bin/activate
fi

python redops.py $TARGET --passive --active --enum --vuln --access --priv --persist --exfil --lateral --beacon --uac --eicar
"""

# Write and chmod
scenario_path.write_text(scenario_script.strip())
scenario_path.chmod(0o755)

# Zip the entire RedOps directory
shutil.make_archive(zip_path.with_suffix('').as_posix(), 'zip', redops_dir.as_posix())

print(f"[✔] Scenario script created at: {scenario_path.resolve()}")
print(f"[✔] RedOps zipped archive created at: {zip_path.resolve()}")

