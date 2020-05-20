## About the *niiview* Project

*niiview* is a python based tool, which can **display 3D and 4D .nii and .nii.gz 
files in terminals with sixel support.** In it's default mode, *niiview* shows the 
middle of a given NIfTI image and prints out basic information about it. 
The tool also has an interactive mode, which enables the user to go through the 
different slices of the brain with the keyboard.

It is based on the idea of https://github.com/MIC-DKFZ/niicat

## How to Install

To install *niiview* into a virtual environment, you can run this commands:
```
python3 -m venv ~/.venv/niiview
. ~/.venv/niiview/bin/activate
pip3 install git+https://jugit.fz-juelich.de/inm7/infrastructure/loony_tools/niiview
niiview file.nii.gz
```

## Problem handling

In case you are experiencing problems with the use of *niiview*, make sure that you
are using a terminal, that supports sixel.
niiview was tested with xterminal.