import subprocess
import time

# Number of worker processes to start
number_of_workers = 10 

# Inform user that workers are being launched
print(f"🚀 Group 35: Launching {number_of_workers} parallel workers...")

# Create multiple worker processes
for i in range(number_of_workers):
    # Start a new worker process
    subprocess.Popen(["python", "worker.py"])
    print(f"✅ Worker {i+1} started.")

# Tell user where to view results
print("🔥 Check http://127.0.0.1:5000/ to see results!")
