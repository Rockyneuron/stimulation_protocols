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
sys.path.append('../../')
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
  
def main():

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
    
    #Experiment parameters
    MON_DISTANCE = 60  # Distance between subject's eyes and monitor
    MON_WIDTH = 50  # Width of your monitor in cm
    MON_SIZE = [1024, 768]  # Pixel-dimensions of your monitor
    MON_HZ=60.01 #Monitor frame rate in Hz 
    FIX_HEIGHT = 100  # Text height of fixation cross
    stimulus_duration=5    #in seconds
    insterstimulus_duration=1
    hello_window_duration=10
    goodbye_window_duration=10
    INITIAL_BASELINE=180
    FINAL_BASELINE=180
    STIMULUS_FRAMES=round(MON_HZ*stimulus_duration)
    INTERSTIMULUS_FRAMES=round(MON_HZ*insterstimulus_duration)
    randomize_image=False   # True or false to randomize images in objets folder
    DRIFT_CORRECTION=True
    INTERSTIMULUS=False

    # Set up LabStreamingLayer stream.
    info = StreamInfo(name='DataSyncMarker', type='Tags', channel_count=1,
                      channel_format='string', source_id='12345') 
    outlet = StreamOutlet(info)  # Broadcast the stream.

    # Set up Pupil Core
    cm.check_capture_exists(ip_address='127.0.0.1',port=50020)
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
        monitor=None,
        color=(110,110,110),
        colorSpace='rgb255',
    )

    # Get list of randomized images.
    images_list=os.listdir(Path('OBJECTS'))   
    images_list=[im for im in images_list if '.tif' or '.jpg' in im] 


    # If we are on a windows sistem remove thumbs.db cache file
    if 'Thumbs.db' in images_list:
        images_list.remove('Thumbs.db')

    #Get list of pseudorandom images
    try:
        images_psedorand=os.listdir(Path('OBJECTS/pseudorandom'))
    except FileNotFoundError:
        print('There is no pseudorandom folder, experiment without surprise')
        if randomize_image:
            random.shuffle(images_list)
        images=[Path('OBJECTS/' + im) for im in images_list]
    else:
        images_psedorand=[im for im in images_psedorand if '.tif' in im]
        print('Experiment with pseudorandom images')

        with open(Path('OBJECTS/pseudorandom/order.txt'),'r') as file:
            for line in file:
                order=line.split(',')
        order_pseudorand=list(map(int,order)) 

        if randomize_image:
            random.shuffle(images_psedorand)
            random.shuffle(images_list)
        
        images=[Path('OBJECTS/' + im) for im in images_list]
        images_psedorand_dir=[Path('OBJECTS/pseudorandom/'+ im) for im in images_psedorand]

        # Insert pseudorandom images in the order stablished
        for loc, im_dir, im in zip(order_pseudorand,images_psedorand_dir,images_psedorand):
            images.insert(loc,im_dir)
            images_list.insert(loc,im)
    finally:
        pass
    
    hello_image=visual.ImageStim(win,image='script_images/Bienvenida_.tiff')
    goodbye_image=visual.ImageStim(win,image='script_images/Final_.tiff')
    # Generate stimulus objects
    drift_point = visual.Circle(win=win,
                                    units="pix",
                                    radius=15,
                                    fillColor=[-1]*3,
                                    lineColor=[-1]*3,
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

    # Let everythng settle and say hello
    for frame in range(round(hello_window_duration*MON_HZ)):
        hello_image.draw()
        win.flip()
    
    print('Press "Enter" to start the calibration')
    cal=True
    cal_finish='ok'
    while cal:
        if keyboard.read_key()=='enter':

            print('starting calibration')
            # Call to pupil API, check problem with display id
            request = {'subject': 'calibration.should_start', 'disp_id': 0} 
            response=p.notify(request)
            win.flip()
            ### uncomment if calubration screen doesnt appear
            # sleep(2)
            # win.winHandle.minimize() 
            # win.winHandle.set_fullscreen(False)
            # win.winHandle.set_fullscreen(True)
            # win.winHandle.maximize()
            # win.flip()
        
            # Check if the calibration process was successfully started
            if response == 'Message forwarded.':
                print('Calibration process started')
            else:
                raise ConnectionError

            #restart calibration if necesary
            while True:
                try:
                    user_input=input('Is the calibration ok? type "ok" to continue or "repeat" to restart: \n')  
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
            print('You have pressed another key. Press control+c to skip program')
    
    start_input='start'
    stim=True
    while stim:
        user_input=input('Type "start" to begin stimulation: \n')
        if start_input==user_input:
            cm.tic()
            print('Starting stimulation...\n initial baseline: ')
            
            annotation=p.new_annotation('baseline_ini_start')
            p.send_annotation(annotation)
            outlet.push_sample(['baseline_ini_start'])
            
            sleep(INITIAL_BASELINE)

            annotation=p.new_annotation('baseline_ini_end')
            p.send_annotation(annotation)
            outlet.push_sample(['baseline_ini_end'])

            print(f'baseline_time:')
            cm.toc()
            stim=False
        elif start_input!=user_input:
            print('Wrong input. Press control+c to skip program')
        else:
            raise ValueError("You have to input a string") 

    for im_number, image_stim in enumerate(image_stim_vec):
        
        cm.tic()
        win.flip()
        annotation=p.new_annotation('blank_{}'.format(im_number))
        p.send_annotation(annotation)
        outlet.push_sample(['blank_{}'.format(im_number)])

        #Interstimulus
        if INTERSTIMULUS:
            for frame in range(INTERSTIMULUS_FRAMES-1):
                win.flip()
            print('interstimulus time blank:')  
            cm.toc()

            cm.tic()
            drift_point.draw()
            win.flip()
            annotation=p.new_annotation('drift_point_{}'.format(im_number))
            p.send_annotation(annotation)
            outlet.push_sample(['drift_point_{}'.format(im_number)])

        if DRIFT_CORRECTION:
            for frame in range(INTERSTIMULUS_FRAMES-1):
                drift_point.draw()
                win.flip()
            print('interstimulus time drift correction:')
            cm.toc()
                        
            cm.tic()
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
        print('stimulus time:')
        cm.toc()

    annotation = p.new_annotation('EndOfExperiment')
    p.send_annotation(annotation)
    outlet.push_sample(['EndOfExperiment'])

    win.flip()

    cm.tic()
    print('final_baseline')
    annotation=p.new_annotation('baseline_end_start')
    p.send_annotation(annotation)
    outlet.push_sample(['baseline_end_start'])

    sleep(FINAL_BASELINE)

    annotation=p.new_annotation('baseline_end_end')
    p.send_annotation(annotation)
    outlet.push_sample(['baseline_end_end'])

    print(f'final baseline time:')
    cm.toc()

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

    for frame in range(round(goodbye_window_duration*MON_HZ)):
        goodbye_image.draw()
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
    cm.save_list_to_txt(images_list,target_dir.joinpath('assets.txt'))
                     
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

