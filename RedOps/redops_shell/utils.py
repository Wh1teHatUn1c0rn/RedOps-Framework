from rich.console import Console
from rich.table import Table

console = Console()

def display_banner():
    console.print("""
[bold red]
 ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗██╗   ██╗███████╗    ██╗   ██╗███╗   ██╗ ██╗ ██████╗ ██████╗ ██████╗ ███╗   ██╗
██╔═══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝██║██║   ██║██╔════╝    ██║   ██║████╗  ██║███║██╔════╝██╔═══██╗██╔══██╗████╗  ██║
██║   ██║█████╗  █████╗  █████╗  ██╔██╗ ██║███████╗██║██║   ██║█████╗      ██║   ██║██╔██╗ ██║╚██║██║     ██║   ██║██████╔╝██╔██╗ ██║
██║   ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║╚════██║██║╚██╗ ██╔╝██╔══╝      ██║   ██║██║╚██╗██║ ██║██║     ██║   ██║██╔══██╗██║╚██╗██║
╚██████╔╝██║     ██║     ███████╗██║ ╚████║███████║██║ ╚████╔╝ ███████╗    ╚██████╔╝██║ ╚████║ ██║╚██████╗╚██████╔╝██║  ██║██║ ╚████║
 ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝  ╚══════╝     ╚═════╝ ╚═╝  ╚═══╝ ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

 ██████╗██████╗ ███████╗██╗    ██╗                                                                                                   
██╔════╝██╔══██╗██╔════╝██║    ██║                                                                                                   
██║     ██████╔╝█████╗  ██║ █╗ ██║                                                                                                   
██║     ██╔══██╗██╔══╝  ██║███╗██║                                                                                                   
╚██████╗██║  ██║███████╗╚███╔███╔╝                                                                                                   
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝                                                                                                    
[/bold red]
[bold white]Modular Red Teaming Shell - RedOps CLI[/bold white]
""", justify="center")

def print_help():
    table = Table(title="RedOps Shell Commands")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_row("set <key> <value>", "Set a value (e.g., set target 192.168.1.1)")
    table.add_row("get <key>", "Get a previously set value")
    table.add_row("run <module>", "Run a module (e.g., run passive)")
    table.add_row("modules", "List available modules")
    table.add_row("creds", "List stored credentials")
    table.add_row("exit", "Exit the shell")
    table.add_row("help", "Show this help message")
    console.print(table)