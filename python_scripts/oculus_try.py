import zmq
import numpy as np
import time

time.sleep(30)

states = ["rest", "left", "right"]
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
    cur_state = states[np.random.choice(np.arange(0, 3), p=[0.5, 0.25, 0.25])]
    print(cur_state)
    socket.send_string(cur_state, flags, copy=copy, track=track)