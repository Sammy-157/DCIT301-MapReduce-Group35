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
    "final_counts": {} # Changed to dict for easier UI reading
}
tasks = []

def run_socket_server():
    global tasks
    try:
        with open("input.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        tasks = ["Default line: Hello world", "Group 35 MapReduce Project"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 6000))
    server.listen(10)

    while tasks:
        conn, addr = server.accept()
        task = tasks.pop(0)
        conn.send(task.encode())
        
        data = conn.recv(1024).decode()
        if data:
            job_data["raw_results"].append(data)
        conn.close()

    # --- Reduce Phase ---
    job_data["status"] = "Map Complete. Reducing..."
    grouped = defaultdict(list)
    for res_str in job_data["raw_results"]:
        try:
            pairs = eval(res_str)
            for word, count in pairs:
                grouped[word].append(count)
        except:
            continue

    # Convert results to a dictionary for the frontend
    reduced_data = {}
    for word, counts in grouped.items():
        reduced_data[word] = sum(counts) # Simple reduction
    
    job_data["final_counts"] = reduced_data
    job_data["status"] = "Finished"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def get_results():
    # Return the dictionary directly to fix the 404/Mapping error
    return jsonify(job_data["final_counts"])

if __name__ == "__main__":
    socket_thread = threading.Thread(target=run_socket_server, daemon=True)
    socket_thread.start()
    app.run(debug=True, port=5000, use_reloader=False)