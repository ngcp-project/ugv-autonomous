
# (c) Copyright, Real-Time Innovations, 2022.  All rights reserved.
# RTI grants Licensee a license to use, modify, compile, and create derivative
# works of the software solely for use with RTI Connext DDS. Licensee may
# redistribute copies of the software provided that all such copies are subject
# to this license. The software is provided "as is", with no warranty of any
# type, including any warranty for fitness for any purpose. RTI is under no
# obligation to maintain or support the software. RTI shall not be liable for
# any incidental or consequential damages arising out of the use or inability
# to use the software.

import time
import sys
import rti.connextdds as dds
from auto_ctrl import auto_ctl
import socket 


class auto_ctlPublisher:

    @staticmethod
    def run_publisher(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, "auto_ctl", auto_ctl)

        # This DataWriter will write data on Topic "Example auto_ctl"
        # DataWriter QoS is configured in USER_QOS_PROFILES.xml
        writer = dds.DataWriter(participant.implicit_publisher, topic)

        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((UDP_IP, UDP_PORT))

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
        heading_error = 0.1

        sample = auto_ctl()      

        for count in range(sample_count):
            # Catch control-C interrupt
            try:
                # Modify the data to be sent here

                
                print(f"Writing auto_ctl, count {count}")
                writer.write(sample)
                time.sleep(1)
            except KeyboardInterrupt:
                break

        print("preparing to shut down...")


if __name__ == "__main__":
    auto_ctlPublisher.run_publisher(
            domain_id=0,
            sample_count=sys.maxsize)
