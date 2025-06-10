import os
import importlib

CORE_DIR = os.path.dirname(__file__)

def list_modules():
    return [f.replace(".py", "") for f in os.listdir(CORE_DIR)
            if f.endswith(".py") and not f.startswith("_") and f not in ["module_loader.py"]]

def load_module(name):
    try:
        return importlib.import_module(f"core.{name}")
    except Exception as e:
        print(f"[!] Failed to import module '{name}': {e}")
        return None