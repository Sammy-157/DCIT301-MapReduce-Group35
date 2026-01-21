import socket
import time
from mapreduce_helper import mapper

def run_worker():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 6000))
            
            task = client.recv(1024).decode()
            if not task:
                break
                
            print(f"Processing: {task.strip()}")
            mapped_data = mapper(task)
            client.send(str(mapped_data).encode())
            client.close()
            time.sleep(0.1) 
        except:
            break

if __name__ == "__main__":
    run_worker()