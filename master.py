from flask import Flask, render_template, jsonify
import socket
import threading
from collections import defaultdict
from mapreduce_helper import reducer

app = Flask(__name__)

# Global variables to track progress
job_data = {
    "status": "Waiting for Workers...",
    "raw_results": [],
    "final_counts": []
}
tasks = []

def run_socket_server():
    global tasks
    try:
        with open("input.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        tasks = ["Default line: Hello world", "Operating Systems project"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 6000))
    server.listen(5)

    while tasks:
        conn, addr = server.accept()
        task = tasks.pop(0)
        conn.send(task.encode())
        
        data = conn.recv(1024).decode()
        job_data["raw_results"].append(data)
        conn.close()

    # --- Reduce Phase ---
    job_data["status"] = "Map Complete. Reducing..."
    grouped = defaultdict(list)
    for res_str in job_data["raw_results"]:
        pairs = eval(res_str)
        for word, count in pairs:
            grouped[word].append(count)

    job_data["final_counts"] = [reducer(word, counts) for word, counts in grouped.items()]
    job_data["status"] = "Finished"

# Web Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(job_data)

if __name__ == "__main__":
    # 1. Start the Socket Server (for Workers) in a background thread
    socket_thread = threading.Thread(target=run_socket_server, daemon=True)
    socket_thread.start()
    
    # 2. Start the Flask Website (for you) on the main thread
    # Note: use_reloader=False is IMPORTANT when using threads!
    app.run(debug=True, port=5000, use_reloader=False)