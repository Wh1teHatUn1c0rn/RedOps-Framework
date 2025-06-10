from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

commands_path = project_root / "RedOps" / "redops_shell" / "commands.py"
commands_path.parent.mkdir(parents=True, exist_ok=True)

# Define the module code
commands_py = """
from rich import print

def run_passive(target):
    print(f"[cyan]Running passive OSINT on {target}...[/cyan]")
    # simulate actual call
    return f"Passive OSINT complete for {target}"

def run_exploit(cve_name):
    print(f"[red]Exploiting CVE: {cve_name}[/red]")
    # simulate actual call
    return f"Exploit {cve_name} simulated"

def show_help():
    help_text = '''
[bold yellow]Available commands:[/bold yellow]
  [green]set target <value>[/green]    - Set current target
  [green]run passive[/green]           - Run passive OSINT
  [green]run exploit <CVE>[/green]     - Simulate CVE exploitation
  [green]exit[/green]                  - Exit the RedOps shell
  [green]help[/green]                  - Show this help message
'''
    print(help_text)
"""

# Write to file
commands_path.write_text(commands_py.strip())

print(f"[✔] Commands module created at: {commands_path.resolve()}")