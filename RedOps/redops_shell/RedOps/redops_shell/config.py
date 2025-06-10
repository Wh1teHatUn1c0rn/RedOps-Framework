# Default configuration for RedOps Shell
current_target = None

# Credential storage (in-memory during session)
credentials = {}

def set_target(target):
    global current_target
    current_target = target

def get_target():
    return current_target

def set_credentials(service, username, password):
    credentials[service] = {"username": username, "password": password}

def get_credentials(service):
    return credentials.get(service)