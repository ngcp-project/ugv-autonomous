
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

DISTANCE_THRESH = 10.0 #10 Ft distance threshold 

payload_string = ""
obstacle_flag = 0
auto_enable = 0

""" temporary Socket Setup before RTI stuff is fleshed out """
host_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_add = "localhost"
host_port = 11112
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

class auto_ctlSubscriber:

    @staticmethod
    def process_data(reader):
        # take_data() returns copies of all the data samples in the reader
        # and removes them. To also take the SampleInfo meta-data, use take().
        # To not remove the data from the reader, use read_data() or read().
        samples = reader.take_data()
        for sample in samples:
            payload_float_list = [round(float(measure),3) for measure in sample.object_dist]
            payload_string_list = [str(round(float(measure),3)) for measure in sample.object_dist]
            print(payload_float_list)

            # If any value is below the distance threshold set obstacle_flag 
            if any(measure <= DISTANCE_THRESH for measure in payload_float_list):
                obstacle_flag = 1
            else:
                obstacle_flag = 0

            udp_payload = f"{velocity_val}, {steering_angle}, {heading_error}, {payload_float_list[0]}, \
                            {payload_float_list[1]}, {payload_float_list[2]}, {payload_float_list[3]}, {payload_float_list[4]}, {auto_enable}, {obstacle_flag}".encode()
            server_socket.sendto(udp_payload, (drive_nucelo_ip, drive_nucelo_port))

            payload_string = " ".join(payload_string_list)  # & convert the returned list to string
            
            print(payload_string, obstacle_flag)
        return len(samples)

    @staticmethod
    def run_subscriber(domain_id: int, sample_count: int):

        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, "auto_ctl", auto_ctl)

        # This DataReader reads data on Topic "Example auto_ctl".
        # DataReader QoS is configured in USER_QOS_PROFILES.xml
        reader = dds.DataReader(participant.implicit_subscriber, topic)

        # Initialize samples_read to zero
        samples_read = 0

        # Associate a handler with the status condition. This will run when the
        # condition is triggered, in the context of the dispatch call (see below)
        # condition argument is not used
        def condition_handler(_):
            nonlocal samples_read
            nonlocal reader
            samples_read += auto_ctlSubscriber.process_data(reader)

        # Obtain the DataReader's Status Condition
        status_condition = dds.StatusCondition(reader)

        # Enable the "data available" status and set the handler.
        status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
        status_condition.set_handler(condition_handler)

        # Create a WaitSet and attach the StatusCondition
        waitset = dds.WaitSet()
        waitset += status_condition

        while samples_read < sample_count:
            # Catch control-C interrupt
            try:
                # Dispatch will call the handlers associated to the WaitSet conditions
                # when they activate
                print("Hello World subscriber sleeping for 1 seconds...")

                waitset.dispatch(dds.Duration(1))  # Wait up to 1s each time
            except KeyboardInterrupt:
                break

        print("preparing to shut down...")


if __name__ == "__main__":
    auto_ctlSubscriber.run_subscriber(
            domain_id=0,
            sample_count=sys.maxsize)
