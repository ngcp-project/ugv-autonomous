import socket
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# CoppeliaSim UDP server address and port
server_address = ('127.0.0.1', 5000)

try:
    while True:
        # Define the integers to send
        int1 = 42
        int2 = 84
        
        # Pack the integers into a message
        message = f"{int1},{int2}".encode('utf-8')
        
        # Send the message
        sock.sendto(message, server_address)
        print(f"Sent: {int1}, {int2}")

        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    sock.close()
