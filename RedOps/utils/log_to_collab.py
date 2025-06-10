from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

utils_path = project_root / "RedOps" / "utils"
utils_path.mkdir(parents=True, exist_ok=True)

# Script content
log_script = """
import requests
import socket

def log_to_collab(operator, module, target, result, server_url="http://localhost:5000/log"):
    data = {
        "operator": operator,
        "module": module,
        "target": target,
        "result": result
    }
    try:
        r = requests.post(server_url, json=data, timeout=5)
        if r.status_code == 200:
            print("[+] Logged to RedOps Collab Server.")
        else:
            print(f"[-] Log failed with status code {r.status_code}")
    except Exception as e:
        print(f"[-] Logging error: {e}")

# Example usage
if __name__ == "__main__":
    log_to_collab(
        operator=socket.gethostname(),
        module="example_module",
        target="192.168.1.10",
        result="success"
    )
"""

# Save script
log_script_path = utils_path / "log_to_collab.py"
log_script_path.write_text(log_script.strip())

print(f"[*] Log utility written to: {log_script_path.resolve()}")
