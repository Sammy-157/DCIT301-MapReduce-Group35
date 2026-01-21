import subprocess
import time

# How many workers do you want to hire?
number_of_workers = 10 

print(f"🚀 Group 35: Launching {number_of_workers} workers together...")

for i in range(number_of_workers):
    # This command starts a worker in the background
    subprocess.Popen(["python", "worker.py"]) 
    print(f"✅ Worker {i+1} joined the system.")

print("\n🔥 All workers are now working in parallel!")
print("Check your browser at http://127.0.0.1:5000 to see the results!")