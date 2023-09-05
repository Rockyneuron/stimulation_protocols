## Stim protocol for pupil labs

Code for presentation of stimulus for the Xscape proyect.
The code automatically executes the stimulation protocol for a 
pupil labs experiment in a display monitor. It automatically connects through
the pupil lab and API, starts the recording and shows the stimulus.
It also sends events to pupil core to record the timstamp in which each event 
was presented.  

To install the environment just execute:

conda env create -f pupil_labs.yml

Once with the environment installed drop the fotos in .tif format you want
for the screen stimulation in OBJECTS. The stimuly from OBJECTS will be randomized,
and the files in OBJECTS/PSEUDORANDOM will be presented in a fixed place but radonmized order
as determined by the order.txt. Where the order is determined by a sequence of numbers seperated by ','.
(0,2,4,5)----order is pythonic where 0 is the first order of appearance.

It might be necesary to play with the parameter screen=(0,1) and to change the main screen in iondows configurations
depending on the computer set up. Dependeding on the computer it may be necesarry to configure the stimulation monitor
as the main screen of the computer, to show the calibration in the stimulation monitor.

With pupil capture executed type
python stim_emotibit.py <dir>

Where dir is the directory to save the stimulation images and a .txt with the order of appearance.
Each .tif will be saved with the following format <image_name>_<order_of_appearance(int)>.tif 


For help type

python stim_emotibit.py -h

Run the program and follow the instruction in the console.


## De code is under development. Any contributions and suggestions are welcome. To 
commit a pull request refer to the Xscape proyect corresponding author: 
arturo-jose.valino@incipit.csic.es

                                            Xscape Project (CSIC-INCIPIT) 02/03/2023
                                            


