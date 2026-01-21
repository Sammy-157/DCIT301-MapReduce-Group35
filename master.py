from flask import Flask, render_template, jsonify
import socket
import threading
from collections import defaultdict

app = Flask(__name__)

# This is where we track everything
job_data = {
    "status": "Waiting for Workers...",
    "completed_count": 0,
    "final_counts": {}
}
raw_results = []
tasks_list = []

def run_socket_server():
    global tasks_list, raw_results
    try:
        with open("input.txt", "r") as f:
            tasks_list = [line.strip() for line in f.readlines() if line.strip()]
    except:
        tasks_list = ["Line 1: Group 35", "Line 2: OS Project", "Line 3: MapReduce"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 6000))
    server.listen(10)

    while tasks_list:
        conn, addr = server.accept()
        task = tasks_list.pop(0)
        conn.send(task.encode())
        
        data = conn.recv(4096).decode()
        if data:
            raw_results.append(data)
            # THIS UPDATES THE COUNTER
            job_data["completed_count"] = len(raw_results)
        conn.close()

    # --- Reduce Phase ---
    job_data["status"] = "Reducing..."
    grouped = defaultdict(list)
    for res_str in raw_results:
        try:
            pairs = eval(res_str)
            for word, count in pairs:
                grouped[word].append(count)
        except: continue

    job_data["final_counts"] = {w: sum(c) for w, c in grouped.items()}
    job_data["status"] = "Finished!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def get_results():
    # We send a clean package to the HTML
    return jsonify({
        "words": job_data["final_counts"],
        "completed_count": job_data["completed_count"],
        "status": job_data["status"]
    })

if __name__ == "__main__":
    threading.Thread(target=run_socket_server, daemon=True).start()
    app.run(debug=True, port=5000, use_reloader=False)