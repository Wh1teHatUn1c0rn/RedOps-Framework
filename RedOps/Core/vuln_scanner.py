import re
import os
import json
import time

CVE_FINGERPRINTS = {
    "Apache/2.4.49": {
        "cve": "CVE-2021-41773",
        "desc": "Path traversal and remote code execution",
        "exploit": "https://www.exploit-db.com/exploits/50383"
    },
    "PHP/7.4.0": {
        "cve": "CVE-2019-11043",
        "desc": "Remote code execution via nginx+PHP-FPM",
        "exploit": "https://www.exploit-db.com/exploits/47699"
    },
    "nginx/1.14.0": {
        "cve": "CVE-2019-20372",
        "desc": "HTTP/2 resource exhaustion",
        "exploit": "https://nvd.nist.gov/vuln/detail/CVE-2019-20372"
    }
}

def load_banners(target):
    banner_file = f"output/{target}_banners.txt"
    if not os.path.exists(banner_file):
        print(f"[-] Banner file not found: {banner_file}")
        return []
    with open(banner_file, "r") as f:
        return f.readlines()

def match_cves(banner_lines):
    matches = []
    for line in banner_lines:
        for fingerprint, details in CVE_FINGERPRINTS.items():
            if fingerprint.lower() in line.lower():
                matches.append((fingerprint, details))
    return matches

def scan_vulns(target):
    print(f"\n=== Vulnerability Scan on {target} ===")
    banners = load_banners(target)
    if not banners:
        print("[-] No banners to scan.")
        return

    matched_vulns = match_cves(banners)
    if matched_vulns:
        print(f"[✔] Found potential vulnerabilities:")
        for fp, details in matched_vulns:
            print(f" - {fp} => {details['cve']}: {details['desc']}")
            print(f"   Exploit: {details['exploit']}")
    else:
        print("[+] No known vulnerable banners found")

    # Save output
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_dir = f"output/{target}_{timestamp}/"
    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(save_dir, "vuln_scan.txt"), "w") as f:
        if matched_vulns:
            for fp, details in matched_vulns:
                f.write(f"{fp} => {details['cve']}: {details['desc']}\n")
                f.write(f"Exploit: {details['exploit']}\n\n")
        else:
            f.write("No vulnerabilities found\n")

    print(f"[+] Vulnerability scan saved to: {save_dir}")

# Standalone
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target domain or IP")
    args = parser.parse_args()
    scan_vulns(args.target)
