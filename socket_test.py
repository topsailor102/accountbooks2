import socket
import sys

HOST = '192.168.178.36'
PORT = 3306

print(f"Attempting to connect to {HOST}:{PORT} using raw socket...")

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    # Connect the socket to the port
    result = sock.connect_ex((HOST, PORT))
    
    if result == 0:
        print("Success! Socket connected.")
    else:
        print(f"Failed! Error code: {result}")
        # errno 65 is EHOSTUNREACH (No route to host)
        
    sock.close()
except Exception as e:
    print(f"Exception occurred: {e}")
