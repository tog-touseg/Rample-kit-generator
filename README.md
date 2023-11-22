# Rample kit generator

The goal of this quick and dirty program is to avoid tedious copy/paste and renaming of samples to fit the Rample naming system while being able to preview samples.

A kits/ folder is created at the location where the script/exec is running when *Save* is pressed. **!!! Each time Save is pressed, the folder is fully deleted and recreated !!!**. Full kits data (absolute path location of original samples, kits names etc.) are also saved at the running location as data.pkl and make it possible to restart the program without losing the work already done.

*Save* copies the original sample files into the kits/ folder by creating folders with the *Export* fields as names. Only kits with non empty *Export* field are exported. Ine these folders samples are renamed as "X lY [sample_name.wav]" where X is the SP track and Y the layer (representend by the sample position in the SP tree). See **Usage** section for more detail on operating the porgram.

For compatibility reasons, a tmp.wav file is created for audio  preview.

## Usage

The script requires python 3.10

Launch script with `python3 rample-kit-generator.py`

For windows users you can find a .exe file in the bin/ folder.

The script was not tested under MacOS.

Following dependencies are required:

- tkinter

- simpleaudio

- natsort

- 

- soundfile

![Image](rkg.png?raw=true)

The **Explorer** tree is used to browse (**Browse** button) folders and preview samples (when selected).

The **Kit** tree is used to name the kit for export (**Export**: A0, A1...), but also has a **Tag** field just for convenience.

Selected sample is added to the **SP** trees by pressing Q,W,E,R (works also with A,Z,E,R) keys. Samples can be moved in the tree with mouse wheel, or deleted by righ-clicking.
