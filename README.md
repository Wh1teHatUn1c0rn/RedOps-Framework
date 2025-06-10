# RedOps Framework

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Status](https://img.shields.io/badge/build-stable-green)

**RedOps** is a modular, extensible red teaming and adversary simulation framework designed to help security professionals simulate realistic post-exploitation scenarios, credential harvesting, privilege escalation, lateral movement, evasion, and more.

---

## Features

-  **Modular Shell Interface** with command parsing and autocompletion
-  **Credential Vault** with AES-encrypted secret storage
-  **C2 Dashboard** with real-time agent registration and tasking (via Flask + Socket.IO)
-  **Exploitation Suite** with simulated and real CVE checks (e.g., Log4Shell, ProxyShell, Drupalgeddon2, Struts, Apache Path Traversal)
-  **Bypass Tools** (AMSI, ETW patching, Defender simulation)
-  **Stager Builder** with XOR/AES payload encryption and loader generation
-  **Module Loader** for dynamic loading of core modules
-  **Local CVE Mapping DB** for offline CVE detection
-  **Task CLI** for manual task queuing via `add_task.py`

---

## 📁 Project Structure

RedOps/

├── core/

│ ├── bypass_suite/ # AMSI, ETW, Defender scripts

│ ├── exploits/ # CVE modules (e.g. log4shell.py, drupalgeddon2.py)

│ ├── secrets_vault.py # Encrypted credential storage

│ ├── cred_harvester.py # Simulated credential collection

│ ├── module_loader.py # Dynamic module listing and importing

│ ├── exploiter.py # Nmap scan + CVE match

│ └── data/

│ └── local_cve_map.json

├── stager_builder.py # Payload encryptor + loader generator

├── redops_shell.py # Interactive command-line shell

├── requirements.txt

└── README.md


---

## Getting Started

### 1. Clone the Repository

git clone https://github.com/your-org/redops-framework.git
cd redops-framework

pip install -r requirements.txt

Requires: nmap, searchsploit, requests, cryptography, flask, flask-socketio, eventlet

python redops_shell.py

cd redops_c2
python app.py

## Example Usage (RedOps Shell)

redops> set target 10.10.10.1
redops> run exploit log4shell
redops> set creds winrm_dc user=admin pass=Passw0rd ip=10.10.10.2
redops> show creds
redops> run cred_harvest

## Simulated CVE Modules

| Exploit               | CVE ID         | Status    |
| --------------------- | -------------- | ----------|
| Log4Shell             | CVE-2021-44228 | Simulated |
| ProxyShell            | CVE-2021-34473 | Simulated |
| Drupalgeddon2         | CVE-2018-7600  | Simulated |
| Apache Struts OGNL    | CVE-2017-5638  | Simulated |
| Apache Path Traversal | CVE-2021-41773 | Simulated |

# All modules run in safe/simulated mode by default. Modify as needed in lab environments.

## Credential Vault

Uses cryptography.fernet for secure AES-based storage of secrets.

from core.secrets_vault import save_secret, load_secret

save_secret("winrm_dc", {"user": "admin", "pass": "RedOps123"})
print(load_secret("winrm_dc"))

## C2 Features

- Flask + Socket.IO real-time dashboard

- Agent registration, tasking, and result callbacks

- Task queuing via API or CLI (add_task.py)

## Contributing

1. Fork the repo

2. Create a new module in core/exploits/

3. Register optional CLI entry in redops_shell.py or use module_loader

## Disclaimer

# RedOps is for legal use only. Do not use against systems you do not own or have explicit permission to test.

## Contact

Have questions or suggestions?

Email: offensiveunicorncrew@pm.me

