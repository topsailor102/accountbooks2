import socket
import sys

HOST = '192.168.178.36'
PORT = 3306
TIMEOUT = 20

print(f"Testing socket.create_connection to {HOST}:{PORT} with timeout {TIMEOUT}...")

try:
    # This is what pymysql calls internally
    sock = socket.create_connection((HOST, PORT), TIMEOUT)
    print("Success! Socket connected.")
    
    # Check what address we actually connected to
    print(f"Connected to: {sock.getpeername()}")
    
    sock.close()
except OSError as e:
    print(f"OSError caught: {e}")
    print(f"Error code: {e.errno}")
except Exception as e:
    print(f"Exception caught: {e}")
