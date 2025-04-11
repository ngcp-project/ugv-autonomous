
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
import array

class auto_ctlPublisher:

    @staticmethod
    def run_publisher(domain_id: int, sample_count: int):

        DISTANCE_THRESH = 10.0

        payload_string = ""
        obstacle_flag = 0
        auto_enable = 0

        """ temporary Socket Setup before RTI stuff is fleshed out """
        host_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_add = "localhost"
        host_port = 11111
        host_sock.bind((host_add, host_port))
        # A DomainParticipant allows an application to begin communicating in
        # a DDS domain. Typically there is one DomainParticipant per application.
        # DomainParticipant QoS is configured in USER_QOS_PROFILES.xml
        participant = dds.DomainParticipant(domain_id)

        # A Topic has a name and a datatype.
        topic = dds.Topic(participant, "auto_ctl", auto_ctl)

        # This DataWriter will write data on Topic "Example auto_ctl"
        # DataWriter QoS is configured in USER_QOS_PROFILES.xml
        writer = dds.DataWriter(participant.implicit_publisher, topic)

        sample = auto_ctl()        

        for count in range(sample_count):
            # Catch control-C interrupt
            try:
                # Modify the data to be sent here
                data, addr = host_sock.recvfrom(1024)
                payload = data.decode() # Convert Byte array to python string type 
                print(payload)
                payload = payload.split(",")  # Parse string using comma delimiter
                resized_payload = payload[2:7] # Only take the middle 5 elements of the list [2, 7)
                payload_float_list = [float(measure) for measure in resized_payload] # Convert string elements to float elements so that they can be used for comparison
                
                # If any value is below the distance threshold set obstacle_flag 
                if any(measure <= DISTANCE_THRESH for measure in payload_float_list):
                    obstacle_flag = 1
                else:
                    obstacle_flag = 0
                
                sample.object_dist = array.array("f", payload_float_list)
                sample.obstacle_flag = obstacle_flag
                            
                #print(f"Writing auto_ctl, count {count}")
                writer.write(sample)
                # time.sleep(1)
            except KeyboardInterrupt:
                break

        print("preparing to shut down...")


if __name__ == "__main__":
    auto_ctlPublisher.run_publisher(
            domain_id=0,
            sample_count=sys.maxsize)
