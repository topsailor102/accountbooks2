import socket
import sys

HOST = '192.168.178.36'
PORT = 3306

print(f"Connecting to {HOST}:{PORT}...")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(20)
    sock.connect((HOST, PORT))
    print("Connected! Waiting for greeting...")
    
    # MySQL server sends a greeting packet immediately after connection
    data = sock.recv(1024)
    if data:
        print(f"Received {len(data)} bytes: {data[:50]}...")
    else:
        print("Received no data (server closed connection?)")
        
    sock.close()
except Exception as e:
    print(f"Error: {e}")
