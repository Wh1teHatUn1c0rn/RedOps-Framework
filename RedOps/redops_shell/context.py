from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

# Set target file path
context_path = project_root / "RedOps" / "redops_shell" / "context.py"
context_path.parent.mkdir(parents=True, exist_ok=True)

# File content
context_code = """
# redops_shell/context.py

class ShellContext:
    def __init__(self):
        self.vars = {}

    def set(self, key, value):
        self.vars[key] = value

    def get(self, key):
        return self.vars.get(key, None)

    def all(self):
        return self.vars
"""

context_path.write_text(context_code.strip())

print(f"[✔] Context module created at: {context_path.resolve()}")