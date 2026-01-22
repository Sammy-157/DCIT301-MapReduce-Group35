import socket
import time
from mapreduce_helper import mapper

# This function runs the worker process
def run_worker():
    while True:
        try:
            # Create a socket for communication with the master
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the master server on port 6000
            client.connect(('localhost', 6000))
            
            # Receive a task (line of data) from the master
            task = client.recv(1024).decode()

            # If no task is received, stop working
            if not task:
                break
                
            # Display task being processed (for monitoring)
            print(f"Processing: {task.strip()}")

            # Apply the MAP function to the task
            mapped_data = mapper(task)

            # Send mapper output back to the master
            client.send(str(mapped_data).encode())

            # Close the connection after task completion
            client.close()

            # Short delay to avoid overloading the server
            time.sleep(0.1)

        except:
            # Stop worker if connection fails or master stops
            break

# Start the worker
if __name__ == "__main__":
    run_worker()
