import psychopy.visual
import psychopy.event
import zmq
import msgpack

# Connect to Pupil Labs recording system
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:50020')

# Create a PsychoPy window
win = psychopy.visual.Window([800, 600], fullscr=False)

# Create a fixation cross stimulus
fixation = psychopy.visual.TextStim(win, text='+', color='white', height=0.2)

# Present the fixation cross and send a message to Pupil Labs
fixation.draw()
win.flip()
socket.send(msgpack.packb({'subject': 'start_recording'}))

# Wait for a response from Pupil Labs
response = socket.recv()

# Present your stimuli here, sending messages to Pupil Labs as needed

# End the recording and disconnect from Pupil Labs
socket.send(msgpack.packb({'subject': 'stop_recording'}))
socket.recv()
socket.close()

# Close the PsychoPy window
win.close()
