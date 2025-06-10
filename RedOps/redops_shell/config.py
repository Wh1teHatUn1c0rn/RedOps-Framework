from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

config_path = project_root / "RedOps" / "redops_shell" / "config.py"
config_path.parent.mkdir(parents=True, exist_ok=True)

# Define config.py content
config_code = """
# Default configuration for RedOps Shell
current_target = None

# Credential storage (in-memory during session)
credentials = {}

def set_target(target):
    global current_target
    current_target = target

def get_target():
    return current_target

def set_credentials(service, username, password):
    credentials[service] = {"username": username, "password": password}

def get_credentials(service):
    return credentials.get(service)
"""

config_path.write_text(config_code.strip())

print(f"[✔] RedOps config created at: {config_path.resolve()}")