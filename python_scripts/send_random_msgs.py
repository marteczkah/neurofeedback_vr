"""script that can be used to receive messages from the gameplay and
send infromation back (without the EEG device)"""
import zmq
import numpy as np
import time
from classification_random import classification_random

# waiting time I used before sending messages during final presentation
# time.wait(30) 

print('listening')
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    flags = 0
    copy = True
    track = False
    print("Message received: ", message)
    cur_state = classification_random()
    socket.send_string(cur_state, flags, copy=copy, track=track)