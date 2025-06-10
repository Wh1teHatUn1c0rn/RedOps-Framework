from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'collab.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            operator TEXT,
            module TEXT,
            target TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/log', methods=['POST'])
def log_entry():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    operator = data.get('operator', 'unknown')
    module = data.get('module', 'unknown')
    target = data.get('target', 'unknown')
    result = data.get('result', 'unknown')
    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, operator, module, target, result) VALUES (?, ?, ?, ?, ?)",
              (timestamp, operator, module, target, result))
    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({'status': 'ok'})
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, operator, module, target, result FROM logs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("dashboard.html", logs=rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)