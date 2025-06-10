from prompt_toolkit.completion import WordCompleter

commands = [
    "help", "exit", "set", "run", "show", "clear",
    "passive", "active", "enum", "vuln", "access", "priv",
    "persist", "exfil", "lateral", "beacon", "obfuscate", "uac",
    "eicar", "exploit", "target", "creds"
]

redops_completer = WordCompleter(commands, ignore_case=True)