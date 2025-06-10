from pathlib import Path

import os
import readline
import shlex
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich.console import Console

console = Console()
session = PromptSession(
    history=FileHistory(str(Path.home() / ".redops_history")),
    auto_suggest=AutoSuggestFromHistory()
)

# Available modules
modules = ["passive", "active", "enum", "vuln", "access", "priv", "persist", "exfil", "lateral", "beacon", "obfuscate", "uac", "eicar", "exploit"]

completer = WordCompleter(
    words=[
        "set", "run", "show", "exit", "help", "clear", "list", "creds"
    ] + modules,
    ignore_case=True
)

# Credential store (in-memory)
cred_store = {}
target = None

def handle_command(cmd):
    global target, cred_store

    try:
        tokens = shlex.split(cmd)
        if not tokens:
            return

        cmd = tokens[0]

        if cmd == "exit":
            console.print("[bold red]Exiting RedOps Shell...[/bold red]")
            raise EOFError

        elif cmd == "clear":
            os.system("clear" if os.name != "nt" else "cls")

        elif cmd == "set":
            if len(tokens) >= 3 and tokens[1] == "target":
                target = tokens[2]
                console.print(f"[bold green]Target set to {target}[/bold green]")
            elif len(tokens) >= 3 and tokens[1] == "creds":
                alias = tokens[2]
                cred_data = dict(part.split("=") for part in tokens[3:] if "=" in part)
                cred_store[alias] = cred_data
                console.print(f"[bold yellow]Stored credentials for {alias}[/bold yellow]")
            else:
                console.print("[bold red]Usage: set target <ip> OR set creds <alias> user=... pass=... ip=...[/bold red]")

        elif cmd == "show":
            if len(tokens) == 2 and tokens[1] == "creds":
                for alias, creds in cred_store.items():
                    console.print(f"[bold blue]{alias}:[/bold blue] {creds}")
            else:
                console.print("[bold red]Usage: show creds[/bold red]")

        elif cmd == "del":
            if len(tokens) == 3 and tokens[1] == "creds":
                removed = cred_store.pop(tokens[2], None)
                if removed:
                    console.print(f"[bold red]Removed creds for {tokens[2]}[/bold red]")
                else:
                    console.print(f"[bold red]No such alias: {tokens[2]}[/bold red]")

        elif cmd == "run":
            if not target:
                console.print("[bold red]No target set. Use 'set target <ip/domain>'[/bold red]")
                return
            if len(tokens) != 2:
                console.print("[bold red]Usage: run <module>[/bold red]")
                return
            module = tokens[1]
            if module not in modules:
                console.print(f"[bold red]Unknown module: {module}[/bold red]")
                return
            subprocess.run(["python3", "redops.py", target, f"--{module}"])

        elif cmd == "list":
            console.print("[bold cyan]Available Modules:[/bold cyan]")
            console.print(", ".join(modules))

        elif cmd == "help":
            console.print("""
[bold cyan]RedOps Shell Commands:[/bold cyan]
  [green]set target <ip>[/green]       Set the current target
  [green]set creds <alias> user=... pass=... ip=...[/green]   Save credentials
  [green]show creds[/green]            List stored credentials
  [green]del creds <alias>[/green]     Delete saved credentials
  [green]run <module>[/green]          Execute a RedOps module
  [green]list[/green]                  Show all modules
  [green]help[/green]                  Display this help message
  [green]exit[/green]                  Quit the shell
""")
        else:
            console.print(f"[bold red]Unknown command: {cmd}[/bold red]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

def main():
    console.print("[bold green]Welcome to the RedOps Interactive Shell![/bold green]")
    while True:
        try:
            user_input = session.prompt("redops> ", completer=completer)
            handle_command(user_input)
        except EOFError:
            break
        except KeyboardInterrupt:
            console.print("[yellow]Ctrl+C detected, use 'exit' to quit.[/yellow]")

if __name__ == "__main__":
    main()