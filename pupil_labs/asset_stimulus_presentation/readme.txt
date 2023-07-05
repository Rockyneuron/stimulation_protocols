## Stim protocol for pupil labs

Code for presentation of stimulus for the Xscape proyect.
The code automatically executes the stimulation protocol for a 
pupil labs + Emotibit experiment with real assets. It automatically connects through
the pupil lab and API, starts the recording. It then radomises the assets 
present in assets.txt and outputs another .txt with the order of the assets.
It also sends events to pupil core to record the timstamp in which each event 
was presented.  
The code also enables to send to events thorugh and LSL to Emotibit and pupil for multiple 
device synchrony. However the code runs perfectly only with pupil labs.

To install the environment just execute:

conda env create -f pupil_labs.yml

With pupil capture executed type
python stim_asset.py <dir>

Where dir is the directory to save the stimulation images and a .txt with the order of appearance.
Each .tif will be saved with the following format <image_name>_<order_of_appearance(int)>.tif 


For help type

python stim_final3 -h

Run the program and follow the instruction in the console.


## De code is under development. Any contributions and suggestions are welcome. To 
commit a pull request refer to the Xscape proyect corresponding author: 
arturo-jose.valino@incipit.csic.es

                                            Xscape Project (CSIC-INCIPIT) 02/03/2023
                                            