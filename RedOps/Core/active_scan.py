import subprocess
import socket
import os
import re
import platform

def is_tool_installed(tool_name):
    return subprocess.call(['which', tool_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan_with_masscan(target):
    print(f"[+] Running masscan on {target}")
    try:
        result = subprocess.check_output(['masscan', '-p1-1024', target, '--rate', '1000'], stderr=subprocess.DEVNULL)
        decoded = result.decode()
        open_ports = re.findall(r'port (\d+)/tcp', decoded)
        print(f"[✔] Open ports: {', '.join(open_ports)}")
        return list(set(int(port) for port in open_ports))
    except Exception as e:
        print(f"[-] masscan error: {e}")
        return []

def scan_with_socket(target):
    print(f"[+] Fallback: scanning top ports manually with socket")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 8080, 8443]
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.create_connection((target, port), timeout=1)
            print(f"[✔] Port {port} open")
            open_ports.append(port)
            sock.close()
        except:
            continue
    return open_ports

def banner_grab(target, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
        data = sock.recv(1024)
        sock.close()
        banner = data.decode(errors='ignore').strip()
        return banner
    except Exception:
        return ""

def os_guess_ttl(target):
    print(f"[+] Guessing OS from ICMP TTL")
    try:
        result = subprocess.check_output(['ping', '-c', '1', target], stderr=subprocess.DEVNULL).decode()
        ttl = re.search(r'ttl=(\d+)', result)
        if ttl:
            ttl_value = int(ttl.group(1))
            if ttl_value >= 128:
                return "Windows (TTL ~128)"
            elif ttl_value >= 64:
                return "Linux/Unix (TTL ~64)"
            elif ttl_value >= 255:
                return "Network Device (TTL ~255)"
            else:
                return f"Unknown TTL: {ttl_value}"
    except:
        return "Could not ping target"
    return "No TTL found"

def recon_active(target):
    print(f"\n=== Active Recon on {target} ===")
    open_ports = []

    if is_tool_installed("masscan"):
        open_ports = scan_with_masscan(target)
    else:
        open_ports = scan_with_socket(target)

    banners = {}
    for port in open_ports:
        banner = banner_grab(target, port)
        if banner:
            banners[port] = banner
            print(f"[BANNER] Port {port}: {banner.splitlines()[0]}")
        else:
            print(f"[BANNER] Port {port}: no banner")

    os_hint = os_guess_ttl(target)
    print(f"[+] OS Guess: {os_hint}")

    # Save results
    save_dir = "output/"
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, f"{target}_active_ports.txt"), "w") as f:
        for port in open_ports:
            f.write(f"{port}\n")
    with open(os.path.join(save_dir, f"{target}_banners.txt"), "w") as f:
        for port, banner in banners.items():
            f.write(f"Port {port}:\n{banner}\n\n")
    with open(os.path.join(save_dir, f"{target}_os_guess.txt"), "w") as f:
        f.write(os_hint + "\n")

    print(f"[+] Active scan results saved to: {save_dir}")

# Standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="IP or hostname to scan")
    args = parser.parse_args()
    recon_active(args.target)
