## Stim protocol for pupil labs

Code for presentation of stimulus for the Xscape proyect.
The code automatically executes the stimulation protocol for a 
pupil labs experiment in a display monitor. It automatically connects through
the pupil lab and API, starts the recording and shows the stimulus.
It also sends events to pupil core to record the timstamp in which each event 
was presented.  

To install the environment just execute:

conda env create -f stimulation_env.yaml

Once with the environment installed drop the fotos in .tif format you want
for the screen stimulation in OBJECTS.

Dependeding on the computer it may be necesarry to configure the stimulation monitor
as the main screen of the compute, to show the calibration in the stimulation monitor.

With pupil capture executed type
python stim_final3.py <dir>

Where dir is the directory to save the stimulation images.

For help type

python stim_final3 -h

Run the program and follow the instruction in the console.


## De code is under development. Any contributions and suggestions
refer to the Xscape proyect corresponding author: arturo-jose.valino@incipit.csic.es

                                            Xscape Project (CSIC-INCIPIT) 02/03/2023
                                            


