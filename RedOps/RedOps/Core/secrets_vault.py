from cryptography.fernet import Fernet
import json
import os

VAULT_KEY_FILE = "core/.vault.key"
VAULT_DATA_FILE = "core/.vault.enc"

def generate_key():
    key = Fernet.generate_key()
    with open(VAULT_KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(VAULT_KEY_FILE):
        return generate_key()
    with open(VAULT_KEY_FILE, "rb") as f:
        return f.read()

def save_secret(label, data):
    key = load_key()
    f = Fernet(key)

    vault = {}
    if os.path.exists(VAULT_DATA_FILE):
        with open(VAULT_DATA_FILE, "rb") as f_enc:
            decrypted = f.decrypt(f_enc.read()).decode()
            vault = json.loads(decrypted)

    vault[label] = data
    with open(VAULT_DATA_FILE, "wb") as f_enc:
        f_enc.write(f.encrypt(json.dumps(vault).encode()))

def load_secret(label):
    key = load_key()
    f = Fernet(key)

    if not os.path.exists(VAULT_DATA_FILE):
        return None

    with open(VAULT_DATA_FILE, "rb") as f_enc:
        decrypted = f.decrypt(f_enc.read()).decode()
        vault = json.loads(decrypted)
        return vault.get(label)