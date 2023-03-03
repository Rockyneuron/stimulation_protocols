#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from psychopy import core, visual
from pyplr.pupil import PupilCore
from pathlib import Path

# ---------------------
# Setup window
# ---------------------
win = visual.Window(
    (900, 900),
    screen=1,
    units="pix",
    allowGUI=True,
    fullscr=True,
)
# ---------------------
# # Example 1: load a stimulus from disk
# # ---------------------

# # assume we're running from the root psychopy repo.
# # you could replace with path to any image:
path_to_image_file = Path('OBJECTS/Asset0001.tif')

# simply pass the image path to ImageStim to load and display:
image_stim = visual.ImageStim(win, image=path_to_image_file)
image_stim.draw()
win.flip()
sleep(2)

path_to_image_file = Path('OBJECTS/Asset0002.tif')
image_stim.draw()
win.flip()

sleep(2)

core.quit()
# # simply pass the image path to ImageStim to load and display:
# image_stim = visual.ImageStim(win, image=path_to_image_file)
# image_stim.draw()

# core.quit()

