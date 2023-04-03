"""Test luminance pre experiment
"""


import sys
sys.path.append('../')

import os
import keyboard
from time import sleep
from psychopy import core, visual, event
from pyplr.pupil import PupilCore
from pathlib import Path
import random
import commons as cm
import argparse
import logging
from pylsl import StreamInfo, StreamOutlet

#Experiment parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 50  # Width of your monitor in cm
MON_SIZE = [1024, 768]  # Pixel-dimensions of your monitor
MON_HZ=60.01 #Monitor frame rate in Hz 

win = visual.Window(
    size=MON_SIZE,
    screen=0,
    units="pix",
    allowGUI=True,
    fullscr=True,
    monitor=None,
    color=(110,110,110),
    colorSpace='rgb255',
)

while True:
    win.flip()
    