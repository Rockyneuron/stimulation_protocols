"""Code for presentation of stimulus fot the Xscape proyect.
The code automatically executes the stimulation protocol for a 
pupil labs experiment. It automatically conects and starts the recording.
It also sends events to pupil core to record the timstamp in which each event 
was presented.  

Raises:
    SystemExit: To cancel the execution
    ConnectionError: If the connection during calibration fails
    ValueError: 

To execute the code it is necessary to type in the console:
python stimulation.py --path <full path for the saved images>"

Outputs:
    1) Saved images in /presented_stimuly in the order of presentation.
        Format: <ObjectName_stim_number.tif>
        Where:
        - ObjectName: is the .tif of each image in OBJECTS dir
        - stim_number= is the stimulus number
    2) /presented_stimuly/assests.txt with the order of presentation of the
    randomised stimuly.
                                    Date: 2/02/2023
                                    Xscape proyect
                                    Corresponding Author: Arturo Valiño                                
"""

import sys
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

def save_list_to_txt(my_list,list_path):
    """Function to save list to a .txt
        Args:
        my_list (_type_): list to save as .txt
        list_path (_type_): fullpath where to save list </.../.../.txt>
    """
    try:
        with open(list_path, mode='x') as f:
            for item in my_list:
                f.write(str(item) + '\n')
    except FileExistsError:
        with open(list_path, mode='w') as f:
            for item in my_list:
                f.write(str(item) + '\n')
    else:
        print('Experiment images saved')            


def main(display_size=(1024,768)):

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
        print("The target directory doesn't exist")
        raise SystemExit(1)

    #Experiment parameters
    MON_DISTANCE = 60  # Distance between subject's eyes and monitor
    MON_WIDTH = 50  # Width of your monitor in cm
    MON_SIZE = [1024, 768]  # Pixel-dimensions of your monitor
    MON_HZ=29.943 #Monitor frame rate in Hz 
    FIX_HEIGHT = 100  # Text height of fixation cross
    stimulus_duration=10    #in seconds
    insterstimulus_duration=2
    STIMULUS_FRAMES=round(MON_HZ*stimulus_duration)
    INTERSTIMULUS_FRAMES=round(MON_HZ*insterstimulus_duration)

    # Set up LabStreamingLayer stream.
    info = StreamInfo(name='DataSyncMarker', type='Tags', channel_count=1,
                      channel_format='string', source_id='12345')
    outlet = StreamOutlet(info)  # Broadcast the stream.

    # Set up Pupil Core
    p = PupilCore()
    
    # ---------------------
    # Setup window
    # ---------------------
    clock = core.Clock()  
    win = visual.Window(
        size=MON_SIZE,
        screen=1,
        units="pix",
        allowGUI=True,
        fullscr=True,
        monitor='LGMonitorXscape',
        color=(110,110,110),
        colorSpace='rgb255',
    )

    # Get list of images.
    images_list=os.listdir(Path('OBJECTS'))   
    # If we are on a windows sistem remove thumbs.db cache file
    images_list.remove('Thumbs.db')
    random.shuffle(images_list)
    images=[Path('OBJECTS/' + im) for im in images_list]
    
    # Generate stimulus objects
    drift_point = visual.Circle(win=win,
                                    units="pix",
                                    radius=50,
                                    fillColor=[-1] * 3,
                                    lineColor=[-1] * 3,
                                    edges=128
                                    )
    # Reallocate all stimuly in an initial list to optimize stimulation.
    image_stim_vec=[visual.ImageStim(win, image=im) for im in images]

    markers = {
        'event': images,
        'test': ['test_event']
    }

    # Start recording
    p.command('R')
  
    # Prepare and send annotations
    # Start the annotations plugin
    p.notify({"subject": "start_plugin", 
              "name": "Annotation_Capture", 
              "args": {}})

    # Let everythng settle
    sleep(10.)
    
    print('press enter to start calibration')
    cal=True
    cal_finish='ok'
    while cal:
        if keyboard.read_key()=='enter':

            print('starting calibration')
            # Call to pupil API, check problem with display id
            request = {'subject': 'calibration.should_start', 'disp_id': 0} 
            response=p.notify(request)
        
            # Check if the calibration process was successfully started
            if response == 'Message forwarded.':
                print('Calibration process started')
            else:
                raise ConnectionError

            #restart calibration if necesary
            while True:
                try:
                    user_input=input('is calibration ok? type "ok" to continue or "repeat" to restart: \n')  
                    if user_input==cal_finish:
                        print('Calibration finished')
                        cal=False
                        break
                    elif user_input=='repeat':
                        break
                    else:
                        print('unrecognised input. type "ok" to continue or "repeat" to restart: \n')
                        continue
                except ValueError:
                    print('Wrong Values') 
        else: 
            print('you have pressed another key. Press control+c tp skip program')
    
    start_input='start'
    stim=True
    while stim:
        user_input=input('type "start" to begin stimulation: \n')
        if start_input==user_input:
            print('starting stimulation...')
            sleep(2)
            stim=False
        elif start_input!=user_input:
            print('Wrong input. Press control+c to skip program')
        else:
            raise ValueError("You have to input a string") 

    for im_number, image_stim in enumerate(image_stim_vec):
        image_stim.draw()
        win.flip()
        annotation = p.new_annotation(images[im_number].name)
        p.send_annotation(annotation)
        outlet.push_sample([markers['event'][im_number].name])

        #Stimulus
        for frame in range(STIMULUS_FRAMES-1):
            image_stim.draw()
            win.flip()
        win.getMovieFrame()        
    
        #Interstimulus
        for frame in range(INTERSTIMULUS_FRAMES):
            drift_point.draw()
            win.flip()

    # Close the window
    win.close()
    
    # Stop recording
    p.command('r')

    # Save stimulation images
    print('Saving stimulation images...')
    win.saveMovieFrames(target_dir.joinpath(' .tif'))

    # Save assets order images
    print('Saving assets order list...')
    save_list_to_txt(images_list,target_dir.joinpath('assets.txt'))
                     
    #Rename saved images
    for asset, saved_stim_images in zip(images_list,os.listdir(target_dir)):
        stimulus_order,_=os.path.splitext(saved_stim_images)
        previous_name=target_dir.joinpath(saved_stim_images)
        asset_number,t_=asset.split('.')
        final_name=asset_number+'_'+stimulus_order.strip() + '.tif'
        previous_name.rename(target_dir / final_name)
    # Close PsychoPy
    core.quit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)

