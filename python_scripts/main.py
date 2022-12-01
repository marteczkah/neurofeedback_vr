"""Sample script for sending data to lsl
Examples:
    $ python lsl_example.py -n Explore_1438
"""

import explorepy

def main():
    # Create an Explore object
    exp_device = explorepy.Explore()

    # Connect to the Explore device using device bluetooth name or mac address
    exp_device.connect(device_name="Explore_855D")

    # Push data to lsl. Note that this function creates three lsl streams, ExG, ORN and marker.
    exp_device.push2lsl()


if __name__ == "__main__":
    main()