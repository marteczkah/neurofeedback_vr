"""Code based on: https://github.com/tne-lab/LSL-inlet/blob/master/lslsendevents.py  """

"""Example program to demonstrate how to send string-valued markers into LSL."""

import random
import time

from pylsl import StreamInfo, StreamOutlet
from classification_random import classification_random


def main():
    # first create a new stream info (here we set the name to MyMarkerStream,
    # the content-type to Markers, 1 channel, irregular sampling rate,
    # and string-valued data) The last value would be the locally unique
    # identifier for the stream as far as available, e.g.
    # program-scriptname-subjectnumber (you could also omit it but interrupted
    # connections wouldn't auto-recover). The important part is that the
    # content-type is set to 'Markers', because then other programs will know how
    #  to interpret the content
    info = StreamInfo('ClassificationResult', 'Markers', 1, 0, 'string', 'myuidw43536')

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending markers...")
    i = 0
    while True:
        # pick a sample to send an wait for a bit
        if i < 10:
            outlet.push_sample([classification_random()])
        else:
            outlet.push_sample(["end"])
        i += 1
        time.sleep(random.random() * 3)


if __name__ == '__main__':
    main()