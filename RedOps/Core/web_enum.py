import requests
import os
import time

def fetch_robots(domain):
    print(f"[+] Checking for robots.txt on {domain}")
    try:
        url = f"http://{domain}/robots.txt"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"[✔] Found robots.txt")
            lines = r.text.splitlines()
            for line in lines:
                print(f"    {line}")
            return r.text
        else:
            print("[-] No robots.txt found")
            return ""
    except Exception as e:
        print(f"[-] Error fetching robots.txt: {e}")
        return ""

def dir_bruteforce(domain, wordlist_path):
    print(f"[+] Starting directory brute-force using {wordlist_path}")
    if not os.path.exists(wordlist_path):
        print(f"[-] Wordlist not found: {wordlist_path}")
        return []

    discovered = []
    with open(wordlist_path, "r") as f:
        for line in f:
            word = line.strip()
            url = f"http://{domain}/{word}"
            try:
                r = requests.get(url, timeout=3)
                if r.status_code not in [404, 403]:
                    print(f"[✔] {url} -> {r.status_code}")
                    discovered.append((url, r.status_code))
            except Exception:
                continue
    return discovered

def enumerate_web(domain):
    print(f"\n=== Web Enumeration on {domain} ===")

    # Results will be saved here
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_dir = f"output/{domain}_{timestamp}/"
    os.makedirs(save_dir, exist_ok=True)

    robots_txt = fetch_robots(domain)
    discovered_dirs = dir_bruteforce(domain, "data/wordlists/common.txt")

    # Save output
    with open(os.path.join(save_dir, "robots.txt"), "w") as f:
        f.write(robots_txt)

    with open(os.path.join(save_dir, "dir_bruteforce.txt"), "w") as f:
        for url, status in discovered_dirs:
            f.write(f"{url} -> {status}\n")

    print(f"[+] Enumeration results saved to {save_dir}")

# Standalone execution
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--wordlist", default="data/wordlists/common.txt", help="Path to wordlist")
    args = parser.parse_args()
    enumerate_web(args.domain)
