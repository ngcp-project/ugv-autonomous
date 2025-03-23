import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

DISTANCE_THRESH = 10.0

payload_string = ""
obstacle_flag = 0
while True:
    data, addr = udp_socket.recvfrom(1024)
    payload = data.decode() # Convert Byte array to python string type 
    payload = payload.split(",")  # Parse string using comma delimiter
    resized_payload = payload[2:7] # Only take the middle 5 elements of the list [2, 7)
    payload_float_list = [float(measure) for measure in resized_payload] # Convert string elements to float elements so that they can be used for comparison
    
    # If any value is below the distance threshold set obstacle_flag 
    if any(measure <= DISTANCE_THRESH for measure in payload_float_list):
        obstacle_flag = 1
    else:
        obstacle_flag = 0

    payload_string = " ".join(resized_payload)  # & convert the returned list to string
    
    print(payload_string, obstacle_flag)