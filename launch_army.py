import subprocess
import time

number_of_workers = 10 
print(f"🚀 Group 35: Launching {number_of_workers} parallel workers...")

for i in range(number_of_workers):
    subprocess.Popen(["python", "worker.py"])
    print(f"✅ Worker {i+1} started.")

print("🔥 Check http://127.0.0.1:5000/ to see results!")