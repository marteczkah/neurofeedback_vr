import explorepy
from explorepy.stream_processor import TOPICS
import time
import zmq
import numpy as np
import simplejson


def my_exg_function(packet):
    message = socket.recv()
    print("Message received: ", message)
    """A function that receives ExG packets and does some operations on the data"""
    t_vector, exg_data = packet.get_data()
    print("Received an ExG packet with data shape: ", exg_data.shape)
    exg_list = exg_data.tolist()
    message_blob = simplejson.dumps(exg_list).encode(encoding="UTF-8")
    flags = 0
    copy = True
    track = False
    socket.send(message_blob, flags, copy=copy, track=track)
    time.sleep(0.125)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Create an Explore object
exp_device = explorepy.Explore()

# Connect to the Explore device using device bluetooth name or mac address
exp_device.connect(device_name="Explore_855D")

# Subscribe your function to the stream publisher
exp_device.stream_processor.subscribe(callback=my_exg_function, topic=TOPICS.raw_ExG)
i = 0

try:
    while True:
        time.sleep(0.125)
except KeyboardInterrupt:
    pass
