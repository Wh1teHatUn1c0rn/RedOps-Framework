from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
module_loader_path = project_root / "RedOps" / "Core" / "module_loader.py"
module_loader_path.parent.mkdir(parents=True, exist_ok=True)

module_loader_code = """
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
"""

module_loader_path.write_text(module_loader_code.strip(), encoding="utf-8")

print(f"[✔] module_loader.py created at: {module_loader_path.relative_to(project_root)}")