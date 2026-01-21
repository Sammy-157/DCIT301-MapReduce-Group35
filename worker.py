import socket
import time
from mapreduce_helper import mapper

def run_worker():
    print("🚀 Worker connected and looking for tasks...")
    
    while True:
        # Create a new socket for each task request
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('localhost', 6000))
            
            # Receive task from Master
            task = client.recv(1024).decode()
            
            # Check if there is still work to do
            if not task or task == "FINISHED":
                print("🏁 No more tasks. Worker shutting down.")
                break
            
            print(f"📦 Processing: {task.strip()}")
            
            # Perform the MAP work
            mapped_data = mapper(task)
            
            # Send result back to Master
            result_str = str(mapped_data)
            client.send(result_str.encode())
            
            # Short break to prevent CPU overloading
            time.sleep(0.1) 
            
        except ConnectionRefusedError:
            print("❌ Master is offline. Stopping...")
            break
        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
            break
        finally:
            client.close()

if __name__ == "__main__":
    run_worker()