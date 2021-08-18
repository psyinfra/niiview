## About *niiview*

*niiview* is a Python3 based tool, which can **display 3D and 4D .nii and
.nii.gz files in terminals with sixel support.** By default, it displays the
middle of a NIfTI image with a selection of simple metrics. An interactive mode
is also available, which allows for keyboard navigation through the different
slices of the brain.

#### Terminals that support sixel:

Sixel is not widely supported among terminals. The following two are known to
work:

* xterminal (in `vt340` mode)
* iTerm2

## Installation

1) makes sure your Terminal can display sixel (see above).
2) install `libsixel` (on Debian/Ubuntu systems:
```
sudo apt install libsixel-bin
```
3) install *niiview* (here we'll use a python virtual environment):
```
python3 -m venv ~/.venv/niiview
source ~/.venv/niiview/bin/activate
pip3 install git+https://github.com/psyinfra/niiview/
niiview file.nii.gz
```

## Troubleshooting

The most common source of problems is getting your terminal to sixel-fy. Make
sure that you are using a terminal that supports sixel, that it's configured
correctly, and that the config is loaded correctly (some systems don't
correctly, for reasons unknown. Sometimes the following helps: `xrdb ~/.Xdefaults`).

*niiview* is a young program, and there are many filetypes and modalities that
it has not been tested with yet. Testing and feedback of failure and success is
much appreciated.

## Inspiration

Credit goes to [niicat](https://github.com/MIC-DKFZ/niicat) for the original
idea to use sixel for quickly inspecting NIfTI images.

Huge thanks to Hayaki Saito, who brought Sixel — a forgotten gem of 80's
technology — forward to modern systems.
