import requests
import socket
import json
import whois
import dns.resolver
import os
import time


def enum_crtsh(domain):
    print(f"[+] Enumerating subdomains via crt.sh")
    subdomains = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        for cert in r.json():
            for entry in cert['name_value'].split('\n'):
                if domain in entry:
                    subdomains.add(entry.strip())
    except Exception as e:
        print(f"[-] crt.sh error: {e}")
    return subdomains


def enum_alienvault(domain):
    print(f"[+] Enumerating subdomains via AlienVault OTX")
    subdomains = set()
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", headers=headers,
                         timeout=10)
        data = r.json()
        for record in data.get('passive_dns', []):
            hostname = record.get('hostname')
            if hostname and domain in hostname:
                subdomains.add(hostname.strip())
    except Exception as e:
        print(f"[-] AlienVault error: {e}")
    return subdomains


def enum_shodan(domain, api_key=None):
    if not api_key:
        print("[!] Skipping Shodan enumeration (no API key provided)")
        return set()
    print(f"[+] Enumerating IPs via Shodan API")
    ip_set = set()
    try:
        r = requests.get(f"https://api.shodan.io/dns/domain/{domain}?key={api_key}", timeout=10)
        data = r.json()
        for sub in data.get('subdomains', []):
            full_sub = f"{sub}.{domain}"
            ip_set.add(full_sub)
    except Exception as e:
        print(f"[-] Shodan error: {e}")
    return ip_set


def perform_whois(domain):
    print(f"[+] Performing WHOIS lookup")
    try:
        w = whois.whois(domain)
        return w.text
    except Exception as e:
        print(f"[-] WHOIS error: {e}")
        return ""


def query_dns(domain):
    print(f"[+] Querying DNS records")
    records = {"A": [], "NS": [], "MX": [], "TXT": []}
    try:
        for record_type in records.keys():
            try:
                answers = dns.resolver.resolve(domain, record_type, lifetime=5)
                for rdata in answers:
                    records[record_type].append(str(rdata))
            except Exception:
                continue
    except Exception as e:
        print(f"[-] DNS query error: {e}")
    return records


def save_results(domain, subdomains, whois_data, dns_records):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_dir = f"output/{domain}_{timestamp}"
    os.makedirs(base_dir, exist_ok=True)

    with open(os.path.join(base_dir, "subdomains.txt"), "w") as f:
        for sub in sorted(subdomains):
            f.write(sub + "\n")

    with open(os.path.join(base_dir, "whois.txt"), "w") as f:
        f.write(whois_data or "No WHOIS data found.")

    with open(os.path.join(base_dir, "dns_records.json"), "w") as f:
        json.dump(dns_records, f, indent=4)

    print(f"[+] Results saved to: {base_dir}")


def recon_passive(domain, shodan_api_key=None):
    print(f"\n=== Passive Recon: {domain} ===")

    crtsh_subs = enum_crtsh(domain)
    alienvault_subs = enum_alienvault(domain)
    shodan_subs = enum_shodan(domain, shodan_api_key)

    all_subdomains = sorted(set(crtsh_subs | alienvault_subs | shodan_subs))
    print(f"\n[✔] Total subdomains found: {len(all_subdomains)}")
    for sub in all_subdomains:
        print(f" - {sub}")

    whois_info = perform_whois(domain)
    dns_info = query_dns(domain)

    save_results(domain, all_subdomains, whois_info, dns_info)


# Allow standalone testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain")
    parser.add_argument("--shodan", help="Optional Shodan API key", default=None)
    args = parser.parse_args()

    recon_passive(args.domain, args.shodan)
