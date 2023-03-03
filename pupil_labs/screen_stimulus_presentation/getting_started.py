"""Getting started with pupil labs network api
"""


# Pupil Remote provides a simple, text-based API to remote control the Pupil Core software
# , as well as to access the second Network API stage (IPC Backbone). It uses ZeroMQ's
#  REQ-REP pattern for reliable one-to-one communication.

#%%
from time import sleep
import zmq

ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
pupil_remote.connect('tcp://127.0.0.1:50020')

#%%
# After opening the REQ socket, you can send simple text messages to control Pupil Capture and Pupil Service functions:
# For every message that
#  you send to Pupil Remote, you need to receive the response. 
# If you do not call recv(), Pupil Capture might become unresponsive!

# start recording
pupil_remote.send_string('R')
print(pupil_remote.recv_string())

# stop recording
sleep(5)
pupil_remote.send_string('r')
print(pupil_remote.recv_string())

""" Availbale comands
'R'  # start recording with auto generated session name
'R rec_name'  # start recording named "rec_name"
'r'  # stop recording
'C'  # start currently selected calibration
'c'  # stop currently selected calibration
'T 1234.56'  # resets current Pupil time to given timestamp
't'  # get current Pupil time; returns a float as string.
'v'  # get the Pupil Core software version string

# IPC Backbone communication
'PUB_PORT'  # return the current pub port of the IPC Backbone
'SUB_PORT'  # return the current sub port of the IPC Backbone
    """


# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()


pub_port

