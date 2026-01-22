from flask import Flask, render_template, jsonify
import socket
import threading
from collections import defaultdict

# Create a Flask web application
app = Flask(__name__)

# This dictionary stores the overall job information
job_data = {
    "status": "Waiting for Workers...",  # Current state of the MapReduce job
    "completed_count": 0,                # Number of completed map tasks
    "final_counts": {}                   # Final reduced output
}

# This list stores raw results sent back by worker nodes
raw_results = []

# This list stores tasks to be sent to workers
tasks_list = []

def run_socket_server():
    global tasks_list, raw_results

    # Read input data (each line is a task)
    try:
        with open("input.txt", "r") as f:
            tasks_list = [line.strip() for line in f.readlines() if line.strip()]
    except:
        # Default data if input file is missing
        tasks_list = ["Line 1: Group 35", "Line 2: OS Project", "Line 3: MapReduce"]

    # Create a TCP socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allows reuse of the same port
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind server to localhost on port 6000
    server.bind(('localhost', 6000))

    # Server can accept up to 10 workers
    server.listen(10)

    # While there are still tasks to give workers
    while tasks_list:
        # Accept a connection from a worker
        conn, addr = server.accept()

        # Send one task to the worker
        task = tasks_list.pop(0)
        conn.send(task.encode())

        # Receive mapper output from worker
        data = conn.recv(4096).decode()
        if data:
            raw_results.append(data)

            # Update number of completed map tasks
            job_data["completed_count"] = len(raw_results)

        # Close connection with worker
        conn.close()

    # ---------------- REDUCE PHASE ----------------
    job_data["status"] = "Reducing..."

    # Group values by key (word)
    grouped = defaultdict(list)

    for res_str in raw_results:
        try:
            pairs = eval(res_str)  # Convert string back to list of (word, count)
            for word, count in pairs:
                grouped[word].append(count)
        except:
            continue

    # Sum all values for each word
    job_data["final_counts"] = {w: sum(c) for w, c in grouped.items()}

    # Job completed
    job_data["status"] = "Finished!"

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# API route to send results to the browser
@app.route('/results')
def get_results():
    return jsonify({
        "words": job_data["final_counts"],
        "completed_count": job_data["completed_count"],
        "status": job_data["status"]
    })

# Start socket server in background and run Flask app
if __name__ == "__main__":
    threading.Thread(target=run_socket_server, daemon=True).start()
    app.run(debug=True, port=5000, use_reloader=False)
