Welcome to your first Connext DDS example!

This Python example was generated using the data type auto_ctl
from auto_ctrl.idl.

This example has one application (auto_ctrl_program.py)
which can run a publisher example (auto_ctrl_publisher.py)
or a subscriber example (auto_ctrl_subscriber.py).

The available examples are:

    - Default example - Basic publisher and subscriber
    - Advanced example (add -exampleTemplate advanced) - Uses an
    		asynchronous generator to read, and monitors status
    		updates in the DataWriter and DataReader.


To Modify the Data:
===================

To modify the data being sent edit the auto_ctrl_publisher.py
file where it says

# Modify the data to be sent here


To Run this Example (command line)
==================================

Run the subscriber on one command prompt:

$ python auto_ctrl_program.py --sub 
or
$ python auto_ctrl_subscriber.py

Run the publisher on a different command prompt:

$ python auto_ctrl_program.py --pub
or
$ python auto_ctrl_publisher.py

You can pass additional arguments. To see the full list:

$ python auto_ctrl_program.py --help

For example, to publish 10 data samples on domain 100, run the following:

$ python auto_ctrl_program.py --pub --domain 100 --sample-count 10



