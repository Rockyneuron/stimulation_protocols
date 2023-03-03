import zmq, msgpack, time

# create a zmq REQ socket to talk to Pupil Service
ctx = zmq.Context()
pupil_remote = ctx.socket(zmq.REQ)
pupil_remote.connect('tcp://localhost:50020')
a=1
 

# set start eye windows
n = {'subject':'eye_process.should_start.0','eye_id': 0, 'args':{}}
print(send_recv_notification(n))
n = {'subject':'eye_process.should_start.1','eye_id':1, 'args':{}}
print(send_recv_notification(n))
time.sleep(2)

# start recording
pupil_remote.send_string('C')
print(pupil_remote.recv_string())

# start recording
pupil_remote.send_string('R')
print(pupil_remote.recv_string())

# set calibration method to hmd calibration
n = {'subject':'start_plugin','name':'HMD_Calibration', 'args':{}}
print(send_recv_notification(n))
time.sleep(2)

# close Pupil Service
n = {'subject':'service_process.should_stop'}
print(send_recv_notification(n))


