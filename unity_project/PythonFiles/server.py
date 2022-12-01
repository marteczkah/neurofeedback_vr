#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import explorepy
from explorepy.stream_processor import TOPICS
import json


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def my_exg_function(packet):
    """A function that receives ExG packets and does some operations on the data"""
    t_vector, exg_data = packet.get_data()
    socket.send(json.dumps(exg_data.tolist()))

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    exp_device = explorepy.Explore()
    exp_device.connect(device_name="Explore_855D")
    exp_device.stream_processor.subscribe(callback=my_exg_function, topic=TOPICS.raw_ExG)

    #  Do some 'work'.
    #  Try reducing sleep time to 0.01 to see how blazingly fast it communicates
    #  In the real world usage, you just need to replace time.sleep() with
    #  whatever work you want python to do, maybe a machine learning task?

