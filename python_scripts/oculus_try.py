import zmq

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
    socket.send("Hello back", flags, copy=copy, track=track)