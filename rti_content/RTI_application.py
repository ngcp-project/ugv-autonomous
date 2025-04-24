import socket

DISTANCE_THRESH = 10.0

payload_string = ""
obstacle_flag = 0
auto_enable = 0

""" temporary Socket Setup before RTI stuff is fleshed out """
host_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_add = "localhost"
host_port = 11111
host_sock.bind((host_add, host_port))

## UDP setup to Tx data to nucelo 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the server to an IP and port (localhost and port 12345 in this case)
server_address = ('192.168.20.5', 12345)  # Replace with your server's IP
server_socket.bind(server_address)

# Define the known client IP and port
drive_nucelo_ip = '192.168.20.21'
drive_nucelo_port = 8   

velocity_val = 0.5
steering_angle = 0
heading_error = 0.0

while True:
    data, addr = host_sock.recvfrom(1024)
    payload = data.decode() # Convert Byte array to python string type 
    payload = payload.split(",")  # Parse string using comma delimiter
    resized_payload = payload[2:7] # Only take the middle 5 elements of the list [2, 7)
    payload_float_list = [float(measure) for measure in resized_payload] # Convert string elements to float elements so that they can be used for comparison
    
    # If any value is below the distance threshold set obstacle_flag 
    if any(measure <= DISTANCE_THRESH for measure in payload_float_list):
        obstacle_flag = 1
    else:
        obstacle_flag = 0

    udp_payload = f"{velocity_val}, {steering_angle}, {heading_error}, {payload_float_list[0]}, \
                    {payload_float_list[1]}, {payload_float_list[2]}, {payload_float_list[3]}, {payload_float_list[4]}, {auto_enable}, {obstacle_flag}".encode()
    server_socket.sendto(udp_payload, (drive_nucelo_ip, drive_nucelo_port))

    payload_string = " ".join(resized_payload)  # & convert the returned list to string
    
    print(payload_string, obstacle_flag)
