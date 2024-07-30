from pupil_labs.realtime_api.simple import Device
from pupil_labs.realtime_api.simple import discover_one_device
import sys
sys.path.append('../../../')
import time
import sys
import os
import keyboard
from time import sleep
from psychopy import core, visual, event
from pathlib import Path
import random
import commons as cm
import argparse
import logging


def main():
    ip = "192.168.235.50"

    # device=Device(address=ip,port=8080)
    device = discover_one_device()

    print(f"Phone IP address: {device.phone_ip}")
    print(f"Phone name: {device.phone_name}")
    print(f"Battery level: {device.battery_level_percent}%")
    print(f"Free storage: {device.memory_num_free_bytes / 1024**3:.1f} GB")
    print(f"Serial number of connected glasses: {device.serial_number_glasses}")
    
    # Start recorsing
    recording_id=device.recording_start()
    print(f"Started recording with id {recording_id}")
    device.send_event("test event 1")

    time.sleep(5)
    device.send_event("test event 2")
    device.recording_stop_and_save()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)

