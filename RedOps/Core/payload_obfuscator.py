import base64

def base64_obfuscate(script_text):
    encoded = base64.b64encode(script_text.encode()).decode()
    wrapper = f'import base64\nexec(base64.b64decode("{encoded}"))'
    return wrapper

def xor_obfuscate(script_text, key=7):
    obfuscated = ','.join([str(ord(c) ^ key) for c in script_text])
    wrapper = (
        f'key={key}\ncode=[{obfuscated}]\n'
        'exec("".join([chr(c ^ key) for c in code]))'
    )
    return wrapper

def obfuscate(script_path, method="base64", output="output/obfuscated.py"):
    with open(script_path, "r") as f:
        original = f.read()

    if method == "base64":
        result = base64_obfuscate(original)
    elif method == "xor":
        result = xor_obfuscate(original)
    else:
        raise ValueError("Unsupported method")

    with open(output, "w") as f:
        f.write(result)
    print(f"[+] Obfuscated payload saved to {output}")
