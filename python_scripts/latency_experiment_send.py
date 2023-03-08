"""Script for the latency experiment where I compare the latency times for the
connection between Python and Unity using ZeroMQ vs LSL."""

import zmq
from pylsl import StreamInfo, StreamOutlet
from classification_random import classification_random
import numpy as np
import pandas as pd
import time
import argparse

# LSL in Unity only worked on Windows
def lsl_experiment(file_name, num_messages=50):
    """Function to send messages through LSL and save the time_stamp in milliseconds
    into a csv file.
    Params:
        - file_name: name of the file where you want to save the experiment results
        - num_messages: number of messages you want to send for the experiment."""
    times = []
    msgs = []
    info = StreamInfo('ClassificationResult', 'Markers', 1, 0, 'string', 'myuidw43536')
    # next make an outlet
    outlet = StreamOutlet(info)

    for i in range(num_messages):
        cur_msg = classification_random()
        outlet.push_sample([cur_msg])
        times.append(round(time.time()*1000))
        msgs.append(cur_msg)
    
    d = {"time_stamp_msg_send" : times, "message" : msgs}
    df = pd.DataFrame(d)
    df.to_csv(file_name)


def zeromq_experiment(file_name, num_messages=50):
    """Function to send messages through ZeroMQ and save the time_stamp in milliseconds
    into a csv file.
    Params:
        - file_name: name of the file where you want to save the experiment results
        - num_messages: number of messages you want to send for the experiment."""
    times = []
    msgs = []
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    num_msgs = 0

    while num_msgs < num_messages:
        message = socket.recv()
        print("Message received: ", message)
        flags = 0
        copy = True
        track = False
        cur_msg = classification_random()
        socket.send_string(cur_msg, flags, copy=copy, track=track)
        times.append(round(time.time()*1000))
        msgs.append(cur_msg)
        num_messages += 1
    
    d = {"time_stamp_msg_send" : times, "message" : msgs}
    df = pd.DataFrame(d)
    df.to_csv(file_name)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("option") 
    parser.add_argument("filename")    
    args = parser.parse_args()
    # print(args.filename, args.option)
    if args.option == "lsl":
        lsl_experiment(args.filename)
    elif args.option == "zeromq":
        zeromq_experiment(args.filename)
        