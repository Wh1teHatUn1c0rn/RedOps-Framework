from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

completer_path = project_root / "RedOps" / "redops_shell" / "completer.py"
completer_path.parent.mkdir(parents=True, exist_ok=True)

# Auto-completion commands list
completer_code = """
from prompt_toolkit.completion import WordCompleter

commands = [
    "help", "exit", "set", "run", "show", "clear",
    "passive", "active", "enum", "vuln", "access", "priv",
    "persist", "exfil", "lateral", "beacon", "obfuscate", "uac",
    "eicar", "exploit", "target", "creds"
]

redops_completer = WordCompleter(commands, ignore_case=True)
"""

# Write to file
completer_path.write_text(completer_code.strip())

print(f"[✔] Command completer module created at: {completer_path.resolve()}")