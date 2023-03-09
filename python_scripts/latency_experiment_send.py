"""Script for the latency experiment where I compare the latency times for the
connection between Python and Unity using ZeroMQ vs LSL."""

import zmq
from pylsl import StreamInfo, StreamOutlet
import pandas as pd
import time
import argparse
import random
import datetime
import random
import string

def generate_random_msg():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# LSL in Unity only worked on Windows
def lsl_experiment(file_name, num_messages):
    """Function to send messages through LSL and save the time_stamp in milliseconds
    into a csv file.
    Params:
        - file_name: name of the file where you want to save the experiment results
        - num_messages: number of messages you want to send for the experiment."""
    time.sleep(10)
    times = []
    msgs = []
    info = StreamInfo('ClassificationResult', 'Markers', 1, 0, 'string', 'myuidw43536')
    # next make an outlet
    outlet = StreamOutlet(info)

    for i in range(num_messages):
        cur_msg = generate_random_msg()
        outlet.push_sample([cur_msg])
        times.append(datetime.datetime.now())
        print(times[-1])
        msgs.append(cur_msg)
        time.sleep(random.random() * 3)
    outlet.push_sample(["end"])
    d = {"time_stamp_msg_send" : times, "message" : msgs}
    df = pd.DataFrame(d)
    df.to_csv(file_name)


def zeromq_experiment(file_name, num_messages):
    """Function to send messages through ZeroMQ and save the time_stamp in milliseconds
    into a csv file.
    Params:
        - file_name: name of the file where you want to save the experiment results
        - num_messages: number of messages you want to send for the experiment."""
    time.sleep(10)
    print("listening")
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
        cur_msg = generate_random_msg()
        socket.send_string(cur_msg, flags, copy=copy, track=track)
        times.append(datetime.datetime.now())
        msgs.append(cur_msg)
        num_msgs += 1
    message = socket.recv()
    socket.send_string("end", flags, copy=copy, track=track)
    d = {"time_stamp_msg_send" : times, "message" : msgs}
    df = pd.DataFrame(d)
    df.to_csv(file_name)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("option") 
    parser.add_argument("filename")    
    parser.add_argument("num_msgs", nargs='?', default=50)
    args = parser.parse_args()
    # print(args.filename, args.option)
    if args.option == "lsl":
        lsl_experiment(args.filename, num_messages=args.num_msgs)
    elif args.option == "zeromq":
        zeromq_experiment(args.filename, num_messages=args.num_msgs)
        