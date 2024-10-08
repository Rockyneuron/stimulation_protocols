import sys
sys.path.append('../../')
import os
import keyboard
from time import sleep
from psychopy import core, visual, event
from pathlib import Path
import random
import commons as cm
import argparse
import logging
from pyplr.pupil import PupilCore
from pylsl import StreamInfo, StreamOutlet
from pupil_labs.realtime_api.simple import Device
from pupil_labs.realtime_api.simple import discover_one_device


def main():
    #Experiment parameters
    stimulus_duration=10    #in seconds

    #Add arguments to indicate where stimulation images will be saved.
    parser=argparse.ArgumentParser(
        prog='Stimulation Protocol',
        description="""Stimulation protocol for XSCAPE proyect. The program runs an 
        randomised stimulation protocol and then saves the images in the provided Path
        in the comand line.""" ,
        epilog="""Rember to enter the path. To execute the program type in the console: 
        python stimulation.py --path <full path for the saved images>""",
        add_help=True,
    )

    parser.add_argument("path")
    args=parser.parse_args()
    target_dir = Path(args.path)

    if not target_dir.exists():
        raise SystemError("The target directory doesn't exist")
    if len(os.listdir(Path(target_dir)))>0:
        raise SystemError('Target directory for saved images is not empty')
  
    # Set up LabStreamingLayer stream.
    info = StreamInfo(name='DataSyncMarker', type='Tags', channel_count=1,
                      channel_format='string', source_id='12345')
    outlet = StreamOutlet(info)  # Broadcast the stream.
    
    # Set up Neon glases
    device = discover_one_device()

    print(f"Phone IP address: {device.phone_ip}")
    print(f"Phone name: {device.phone_name}")
    print(f"Battery level: {device.battery_level_percent}%")
    print(f"Free storage: {device.memory_num_free_bytes / 1024**3:.1f} GB")
    print(f"Serial number of connected glasses: {device.serial_number_glasses}")

    # Get list of assets
    assets=[]
    with open('assets.txt') as file:
        for line in file:
            assets.append(line.replace('\n',''))
    print(assets)

    random.shuffle(assets)
    print(assets)
    print(assets[0])

    markers = {
        'event': assets,
        'test': ['test_event']
    }
    # Start recording
    recording_id=device.recording_start()
    print(f"Started recording with id {recording_id}")
    
    # Prepare and send annotations
    # Start the annotations plugin
   
    start_input='start'
    stim=True
    while stim:
        user_input=input('Type "start" to begin experiment, calibrate manually: \n')
        if start_input==user_input:
            print('Starting stimulation...')
            sleep(2)
            stim=False
        elif start_input!=user_input:
            print('Wrong input. Press control+c to skip program')
        else:
            raise ValueError("You have to input a string") 

    for asset_number, asset in enumerate(assets):
        print(asset_number)
        print(asset)

        print(f'Place asset: {asset} and press enter when ready')
        cal=True
        cal_finish='ok'
        while cal:
            if keyboard.read_key()=='enter':

                cm.tic()
                #Send annotations to LSL and pupil core
                print(f'Recording asset data: {asset}..')

                device.send_event(asset)
                outlet.push_sample([asset])
                sleep(stimulus_duration)

                device.send_event('end_of_stimulation')
                outlet.push_sample(['end_of_stimulation'])

                print('stimulus time:')
                cm.toc() 
                break
            else: 
                print('You have pressed another key. Press control+c to skip program')
    outlet.push_sample(['end_of_experiment'])    
    device.send_event('end_of_experiment')

    finish_input='f'
    final_test=True
    while final_test:
        user_input=input('Do a Test before you end. Type "f" to finish the experiment": \n')
        if finish_input==user_input:
            print('Ending experiment...')
            final_test=False
        elif finish_input!=user_input:
            print('Wrong input. Press control+c to skip program')
        else:
            raise ValueError("You have to input a string")   
    # Stop recording
    device.recording_stop_and_save()
    
    # Save assets order of appearance
    print('Saving assets order list...')
    cm.save_list_to_txt(assets,target_dir.joinpath('assets.txt'))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)
