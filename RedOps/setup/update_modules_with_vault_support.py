from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

update_script_path = project_root / "RedOps" / "setup" / "update_modules_with_vault_support.py"
update_script_path.parent.mkdir(parents=True, exist_ok=True)

update_script_code = '''
from pathlib import Path

# Update initial_access.py
initial_access_path = Path(__file__).resolve().parents[2] / "core" / "initial_access.py"
if initial_access_path.exists():
    with open(initial_access_path, "r") as f:
        ia_code = f.read()

    if "def try_access(domain):" in ia_code:
        ia_code = ia_code.replace(
            "def try_access(domain):",
            "def try_access(domain, username=None, password=None):"
        )

        ia_code += """


# Standalone usage example
if __name__ == '__main__':
    try_access('example.com', username='admin', password='admin123')
"""
        with open(initial_access_path, "w") as f:
            f.write(ia_code.strip())

# Update lateral_movement.py
lateral_path = Path(__file__).resolve().parents[2] / "core" / "lateral_movement.py"
if lateral_path.exists():
    with open(lateral_path, "r") as f:
        lm_code = f.read()

    if "def lateral_movement(target=None):" in lm_code:
        lm_code = lm_code.replace(
            "def lateral_movement(target=None):",
            "def lateral_movement(target=None, ssh_creds=None, winrm_creds=None):"
        )

        insert_logic = """
    if ssh_creds:
        ssh_move(ssh_creds['ip'], ssh_creds['user'], ssh_creds['pass'])

    if winrm_creds:
        winrm_move(winrm_creds['ip'], winrm_creds['user'], winrm_creds['pass'])
"""

        if "# SSH move" in lm_code:
            lm_code = lm_code.replace("# SSH move", insert_logic.strip())

        with open(lateral_path, "w") as f:
            f.write(lm_code.strip())

print("[+] Modules updated successfully with vault credential support.")
'''


update_script_path.write_text(update_script_code.strip())
print(f"[*] Vault updater created at: {update_script_path.resolve()}")