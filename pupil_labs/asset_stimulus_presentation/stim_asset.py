import sys
sys.path.append('../')
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

def main():
    #Experiment parameters
    stimulus_duration=6    #in seconds

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
    
    # Set up Pupil Core
    cm.check_capture_exists(ip_address='127.0.0.1',port=50020)
    p = PupilCore()

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
    p.command('R')
  
    # Prepare and send annotations
    # Start the annotations plugin
    p.notify({"subject": "start_plugin", 
              "name": "Annotation_Capture", 
              "args": {}})
   
    start_input='start'
    stim=True
    while stim:
        user_input=input('Type "start" to begin experiment: \n')
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
                annotation = p.new_annotation(asset)
                p.send_annotation(annotation)
                outlet.push_sample([asset])
                sleep(stimulus_duration)

                annotation = p.new_annotation('end_of_stimulation')
                p.send_annotation(annotation)
                outlet.push_sample(['end_of_stimulation'])

                print('stimulus time:')
                cm.toc() 
                break
            else: 
                print('You have pressed another key. Press control+c to skip program')
    outlet.push_sample(['end_of_experiment'])    
    
    # Stop recording
    p.command('r')
    
    # Save assets order of appearance
    print('Saving assets order list...')
    cm.save_list_to_txt(assets,target_dir.joinpath('assets.txt'))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)
