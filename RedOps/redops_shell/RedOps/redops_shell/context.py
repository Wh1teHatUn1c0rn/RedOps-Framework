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