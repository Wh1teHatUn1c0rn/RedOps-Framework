import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from handlers import *
from utils import display_banner, print_help
from RedOps.redops_shell.RedOps.redops_shell.handlers import handle_set, handle_get, handle_modules, handle_creds
from RedOps.redops_shell.RedOps.redops_shell.completer import redops_completer
from prompt_toolkit import PromptSession
from rich.console import Console

console = Console()


class RedOpsShell:
    def __init__(self):
        self.session = PromptSession(completer=redops_completer)

    def run(self):
        display_banner()
        while True:
            try:
                cmd = self.session.prompt("redops> ").strip()
                if not cmd:
                    continue
                parts = cmd.split()
                command = parts[0]
                args = parts[1:]

                if command == "exit":
                    break
                elif command == "set":
                    handle_set(args)
                elif command == "get":
                    handle_get(args)
                elif command == "modules":
                    handle_modules()
                elif command == "creds":
                    handle_creds()
                elif command == "help":
                    print_help()
                elif command == "run" and len(args) == 1:
                    console.print(f"[bold green]Running module:[/bold green] {args[0]}")
                    # TODO: actual module call
                else:
                    console.print("[red]Invalid command or usage. Type 'help' for options.[/red]")
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Interrupted. Type 'exit' to quit.[/bold yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


if __name__ == "__init__":
    shell = RedOpsShell()
    shell.run()