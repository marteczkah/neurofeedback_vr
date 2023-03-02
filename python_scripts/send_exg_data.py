"""Script to acquire the data from the Mentalab's device and communicate it
with Unity in a form of an array."""

import explorepy
from explorepy.stream_processor import TOPICS
import time
import zmq
import numpy as np
import simplejson


def my_exg_function(packet):
    """A function that receives ExG packets and sends the acquired channels to Unity
    upon request."""
    message = socket.recv()
    print("Message received: ", message)
    t_vector, exg_data = packet.get_data()
    print("Received an ExG packet with data shape: ", exg_data.shape)
    #changing the data format to json for communication
    exg_list = exg_data.tolist()
    message_blob = simplejson.dumps(exg_list).encode(encoding="UTF-8")
    flags = 0
    copy = True
    track = False
    print("Send ExG packet to Unity.")
    socket.send(message_blob, flags, copy=copy, track=track)
    time.sleep(0.125)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Create an Explore object
exp_device = explorepy.Explore()

# Connect to the Explore device using device bluetooth name or mac address
exp_device.connect(device_name="Explore_8435") # change the device name

# Subscribe your function to the stream publisher
exp_device.stream_processor.subscribe(callback=my_exg_function, topic=TOPICS.raw_ExG)
i = 0

try:
    while True:
        time.sleep(0.125)
except KeyboardInterrupt:
    pass
