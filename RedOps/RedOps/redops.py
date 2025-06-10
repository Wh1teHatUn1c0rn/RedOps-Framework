from core.module_loader import list_modules, load_module
from core.secrets_vault import save_secret, load_secret
from utils import log_to_collab
import os
import argparse
import getpass
import json
import subprocess
import platform

from Core import (
    passive_osint, active_scan, web_enum, vuln_scanner,
    initial_access, priv_esc, persistence, exfiltration,
    lateral_movement, c2_beacon,
    payload_obfuscator, uac_bypass_sim, av_evasion, exploiter, bypass_suite
)

def manage_secrets():
    print("\n=== RedOps Vault Secret Manager ===")
    while True:
        print("\nOptions:")
        print("1. Save a new secret")
        print("2. Load and view a secret")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            key = input("Secret name (e.g., ssh_prod_server): ").strip()
            try:
                value = json.loads(input("Enter secret as JSON (e.g., {'ip': '1.2.3.4', 'user': 'admin', 'pass': 'pw'}): "))
                save_secret(key, value)
                print(f"[✔] Saved secret under key: {key}")
            except Exception as e:
                print(f"[-] Error parsing JSON: {e}")

        elif choice == "2":
            key = input("Secret name to load: ").strip()
            try:
                secret = load_secret(key)
                print(f"[+] Secret for '{key}': {json.dumps(secret, indent=2)}")
            except Exception as e:
                print(f"[-] Error: {e}")

        elif choice == "3":
            break
        else:
            print("Invalid option.")

def main():
    parser = argparse.ArgumentParser(description="RedOps Recon Suite - Modular Red Teaming Toolkit")
    parser.add_argument("domain", nargs="?", help="Target domain or IP OR type 'secrets' to manage vault")
    parser.add_argument("--passive", action="store_true", help="Run passive OSINT")
    parser.add_argument("--active", action="store_true", help="Run active scanning")
    parser.add_argument("--enum", action="store_true", help="Run web enumeration")
    parser.add_argument("--vuln", action="store_true", help="Run vulnerability scanner")
    parser.add_argument("--access", action="store_true", help="Attempt initial access")
    parser.add_argument("--priv", action="store_true", help="Run privilege escalation checks")
    parser.add_argument("--persist", action="store_true", help="Establish persistence (simulated)")
    parser.add_argument("--exfil", action="store_true", help="Simulate exfiltration")
    parser.add_argument("--lateral", action="store_true", help="Simulate lateral movement")
    parser.add_argument("--beacon", action="store_true", help="Run C2 beacon simulation")
    parser.add_argument("--obfuscate", help="Obfuscate a Python script (pass path)")
    parser.add_argument("--uac", action="store_true", help="Simulate UAC bypass")
    parser.add_argument("--eicar", action="store_true", help="Generate EICAR test file")
    parser.add_argument('--exploit', action='store_true', help='Run targeted CVE exploitation based on service scan')
    parser.add_argument("--bypass", choices=["amsi", "etw", "defender"], help="Run Bypass Suite techniques")
    parser.add_argument('--shell', action='store_true', help='Launch interactive RedOps shell')
    parser.add_argument("--harvest", action="store_true", help="Simulate credential harvesting")
    parser.add_argument("--list-modules", action="store_true", help="List all available modules in /core")
    parser.add_argument("--run-module", help="Run a specific module from /core")
    parser.add_argument("--offline", action="store_true", help="Run in offline (airgapped) mode")

    args = parser.parse_args()
    operator = getpass.getuser()

    if args.shell:
        try:
            from redops_shell.shell import RedOpsShell
            shell = RedOpsShell()
            shell.cmdloop()
        except Exception as e:
            print(f"[-] Failed to launch RedOps shell: {e}")
        return

    if args.domain == "secrets":
        manage_secrets()
        return

    if args.passive:
        passive_osint.recon_passive(args.domain)
        log_to_collab(operator=operator, module="passive_osint", target=args.domain, result="success")
    if args.active:
        active_scan.recon_active(args.domain)
        log_to_collab(operator=operator, module="active_scan", target=args.domain, result="success")
    if args.enum:
        web_enum.enumerate_web(args.domain)
        log_to_collab(operator=operator, module="web_enum", target=args.domain, result="success")
    if args.vuln:
        vuln_scanner.scan_vulns(args.domain)
        log_to_collab(operator=operator, module="vuln_scanner", target=args.domain, result="success")
    if args.access:
        creds = load_secret("web_login_creds")
        if creds:
            initial_access.try_access(args.domain, creds.get("username"), creds.get("password"))
            log_to_collab(operator=operator, module="initial_access", target=args.domain, result="success")
        else:
            print("[-] No credentials found in vault for 'web_login_creds'")
    if args.priv:
        priv_esc.check_privilege_escalation(args.domain)
        log_to_collab(operator=operator, module="priv_esc", target=args.domain, result="success")
    if args.persist:
        persistence.persist_backdoor(args.domain)
        log_to_collab(operator=operator, module="persistence", target=args.domain, result="success")
    if args.exfil:
        exfiltration.simulate_exfil(args.domain)
        log_to_collab(operator=operator, module="exfiltration", target=args.domain, result="success")
    if args.lateral:
        ssh_creds = load_secret("ssh_prod_server")
        winrm_creds = load_secret("winrm_dc")
        if ssh_creds or winrm_creds:
            lateral_movement.lateral_movement(ssh_creds=ssh_creds, winrm_creds=winrm_creds)
            log_to_collab(operator=operator, module="lateral_movement", target=args.domain, result="success")
        else:
            print("[-] No SSH or WinRM credentials found in vault.")
    if args.beacon:
        c2_beacon.run_beacon()
        log_to_collab(operator=operator, module="c2_beacon", target=args.domain, result="success")
    if args.obfuscate:
        payload_obfuscator.obfuscate(args.obfuscate)
        log_to_collab(operator=operator, module="payload_obfuscator", target=args.obfuscate, result="success")
    if args.uac:
        uac_bypass_sim.simulate_uac_bypass()
        log_to_collab(operator=operator, module="uac_bypass_sim", target=args.domain, result="success")
    if args.eicar:
        av_evasion.generate_masked_eicar()
        log_to_collab(operator=operator, module="av_evasion", target=args.domain, result="success")
    if args.exploit:
        exploiter.run_exploiter(args.domain)
        log_to_collab(operator=operator, module="exploiter", target=args.domain, result="success")
    if args.bypass:
        system = platform.system()
        if system != "Windows":
            print("[-] Bypass suite is designed for Windows systems.")
        else:
            if args.bypass == "amsi":
                subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-File", "core/bypass_suite/amsi_bypass.ps1"])
            elif args.bypass == "etw":
                subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-File", "core/bypass_suite/etw_patch.ps1"])
            elif args.bypass == "defender":
                subprocess.call(["core/bypass_suite/defender_exclude_sim.bat"], shell=True)
    if args.harvest:
        cred_harvester.harvest_creds()
        log_to_collab(operator=operator, module="cred_harvester", target=args.domain, result="success")
    if args.list_modules:
        print("\nAvailable Modules:")
        for mod in list_modules():
            print(f" - {mod}")
        return

    if args.run_module:
        mod = load_module(args.run_module)
        if mod and hasattr(mod, "run"):
            mod.run(args.domain)
            log_to_collab(operator=operator, module=args.run_module, target=args.domain, result="success")
        else:
            print(f"[-] Module '{args.run_module}' not found or has no 'run()' function.")
        return


if __name__ == "__main__":
    main()