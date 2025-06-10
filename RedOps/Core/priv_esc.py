import os
import platform
import subprocess
import stat

def check_linux_suid():
    print("[+] Checking for SUID/SGID binaries...")
    try:
        suid_bins = subprocess.check_output(["find", "/", "-perm", "/4000", "-type", "f", "2>/dev/null"], text=True, stderr=subprocess.DEVNULL)
        lines = suid_bins.strip().split("\n")
        for line in lines:
            if line:
                print(f"[SUID] {line}")
        return lines
    except Exception as e:
        print(f"[-] SUID check failed: {e}")
        return []

def check_writable_shadow():
    print("[+] Checking for writable /etc/shadow...")
    try:
        mode = os.stat("/etc/shadow").st_mode
        writable = bool(mode & stat.S_IWUSR or mode & stat.S_IWGRP or mode & stat.S_IWOTH)
        if writable:
            print("[✔] /etc/shadow is writable!")
            return True
        else:
            print("[i] /etc/shadow is not writable")
    except Exception as e:
        print(f"[-] /etc/shadow check failed: {e}")
    return False

def check_cron_jobs():
    print("[+] Checking for cron jobs...")
    try:
        output = subprocess.check_output("cat /etc/crontab", shell=True, text=True)
        if output:
            print("[✔] Found cron jobs:")
            print(output)
            return output
    except Exception as e:
        print(f"[-] Cron check failed: {e}")
    return ""

def simulate_windows_checks():
    print("[+] Simulating Windows privilege checks...")
    simulated_results = [
        "[UNQUOTED SERVICE PATH] C:\\Program Files\\My App\\service.exe",
        "[SERVICE] Running as SYSTEM",
        "[ADMIN] Current user has admin privileges"
    ]
    for line in simulated_results:
        print(line)
    return simulated_results

def check_privilege_escalation(domain):
    print(f"\n=== Privilege Escalation Simulation on {domain or 'local host'} ===")

    system = platform.system().lower()
    results = []

    if "linux" in system:
        suid_bins = check_linux_suid()
        if check_writable_shadow():
            results.append("/etc/shadow is writable")
        cron_output = check_cron_jobs()
    elif "windows" in system:
        results = simulate_windows_checks()
    else:
        print("[-] Unsupported OS for local privilege check")

    # Save results
    os.makedirs("output", exist_ok=True)
    output_file = f"output/{domain}_priv_esc.txt"
    with open(output_file, "w") as f:
        f.write("Privilege Escalation Results:\n")
        if results:
            for item in results:
                f.write(item + "\n")
        else:
            f.write("No privilege escalation paths found.\n")

    print(f"[+] Results saved to {output_file}")

# Standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain or IP")
    args = parser.parse_args()
    check_privilege_escalation(args.domain)
