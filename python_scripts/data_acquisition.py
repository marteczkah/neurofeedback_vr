import argparse
import explorepy

exp_device = explorepy.Explore()
exp_device.connect(device_name="Explore_1C3B")
exp_device.record_data("c", duration=20, file_type="csv")
