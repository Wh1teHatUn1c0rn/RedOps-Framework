from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent
except NameError:
    project_root = Path.cwd()

handlers_path = project_root / "RedOps" / "redops_shell" / "handlers.py"
handlers_code = """
from redops_shell.state import shell_state
from redops_shell.utils import console, print_help
from core.secrets_vault import list_secrets

def handle_set(args):
    if len(args) >= 2:
        key, value = args[0], " ".join(args[1:])
        shell_state[key] = value
        console.print(f"[green][✔] Set [cyan]{key}[/cyan] = {value}[/green]")
    else:
        console.print("[red][-] Usage: set <key> <value>[/red]")

def handle_get(args):
    if len(args) == 1:
        key = args[0]
        value = shell_state.get(key, None)
        if value:
            console.print(f"[yellow]{key} = {value}[/yellow]")
        else:
            console.print(f"[red][-] Key '{key}' not found[/red]")
    else:
        console.print("[red][-] Usage: get <key>[/red]")

def handle_modules():
    console.print(\"\"\"
[bold cyan]Available Modules:[/bold cyan]
- passive
- active
- enum
- vuln
- access
- priv
- persist
- exfil
- lateral
- beacon
- obfuscate
- uac
- eicar
- exploit
\"\"\")

def handle_creds():
    secrets = list_secrets()
    if secrets:
        console.print("[bold green]Stored Credentials:[/bold green]")
        for name in secrets:
            console.print(f"- {name}")
    else:
        console.print("[yellow]No credentials found in vault.[/yellow]")

def handle_help():
    print_help()
"""

handlers_path.parent.mkdir(parents=True, exist_ok=True)
handlers_path.write_text(handlers_code.strip(), encoding="utf-8")

print(f"[✔] handlers.py created at: {handlers_path.resolve()}")