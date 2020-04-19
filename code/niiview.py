#!/home/tkadelka/env/niicat_env/bin/python3

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nb
from getkey import getkey, keys
from libsixel import *
from PIL import Image
from io import BytesIO



# This function creates the figure, that should be plotted later.
# It is based on: _plot_nifti_preview(iFile, show, return_fig=False, dpi=150)
# from https://github.com/vnckppl/niipre"""
def create_plot( show ):

    # Spacing for Aspect Ratio
    sX = nifti_image.header['pixdim'][1]
    sY = nifti_image.header['pixdim'][2]
    sZ = nifti_image.header['pixdim'][3]

    # Size per slice
    lX = nifti_data.shape[0]
    lY = nifti_data.shape[1]
    lZ = nifti_data.shape[2]

    # True middle point
    tmX = lX / 2.0
    tmY = lY / 2.0
    tmZ = lZ / 2.0

    # Orientation
    qfX = nifti_image.get_qform()[0, 0]
    sfX = nifti_image.get_sform()[0, 0]

    if qfX < 0 and (sfX == 0 or sfX < 0):
        oL = 'R'
        oR = 'L'
    elif qfX > 0 and (sfX == 0 or sfX > 0):
        oL = 'L'
        oR = 'R'
    else:
        oL = ''
        oR = ''

    if sfX < 0 and (qfX == 0 or qfX < 0):
        oL = 'R'
        oR = 'L'
    elif sfX > 0 and (qfX == 0 or qfX > 0):
        oL = 'L'
        oR = 'R'
    else:
        oL = ''
        oR = ''



    # Plot main window
    fig_jpeg = plt.figure(
        facecolor='black',
        figsize=(5, 4),
        dpi=dpi
    )



    # Coronal
    ax1 = fig_jpeg.add_subplot(2, 2, 1)
    imgplot = plt.imshow(
        np.rot90(nifti_data[:, show[1], :]),
        aspect=sZ / sX,
    )
    imgplot.set_cmap('gray')

    ax1.hlines(tmZ, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax1.vlines(tmX, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')

    # Sagittal
    ax2 = fig_jpeg.add_subplot(2, 2, 2)
    imgplot = plt.imshow(
        np.rot90(nifti_data[show[0], :, :]),
        aspect=sZ / sY,
    )
    imgplot.set_cmap('gray')

    ax2.hlines(tmZ, 0, lY, colors='red', linestyles='dotted', linewidth=.5)
    ax2.vlines(tmY, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')

    # Axial
    ax3 = fig_jpeg.add_subplot(2, 2, 3)
    imgplot = plt.imshow(
        np.rot90(nifti_data[:, :, show[2]]),
        aspect=sY / sX
    )
    imgplot.set_cmap('gray')

    ax3.hlines(tmY, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax3.vlines(tmX, 0, lY, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')


    plt.text(-10, show[1] + 5, oL, fontsize=9, color='red')  # Label on left side

    # Textual information
    # sform code
    sform = np.round(nifti_image.get_sform(), decimals=2)
    sform_txt = str(sform).replace('[', ' ').replace(']', ' ').replace(' ', '   ').replace('   -', '  -')

    # qform code
    qform = np.round(nifti_image.get_qform(), decimals=2)
    qform_txt = str(qform).replace('[', ' ').replace(']', ' ').replace(' ', '   ').replace('   -', '  -')

    # Dimensions
    dims = str(nifti_data.shape).replace(', ', ' x ').replace('(', '').replace(')', '')
    dim = ("Dimensions: " + dims)

    # Spacing
    spacing = ("Spacing: "
               + str(np.round(sX, decimals=2))
               + " x "
               + str(np.round(sY, decimals=2))
               + " x "
               + str(np.round(sZ, decimals=2))
               + " mm"
               )

    # Data type
    type = nifti_image.header.get_data_dtype()
    type_str = ("Data type: " + str(type))

    # Volumes
    volumes = ("Volumes: " + str(nifti_image.header['dim'][4]))

    # Range
    min = np.round(np.amin(nifti_data), decimals=2)
    max = np.round(np.amax(nifti_data), decimals=2)
    range = ("Range: " + str(min) + " - " + str(max))

    text = (
            dim + "\n"
            + spacing + "\n"
            + volumes + "\n"
            + type_str + "\n"
            + range + "\n\n"
            + "sform code:\n"
            + sform_txt + "\n"
            + "\nqform code:\n"
            + qform_txt
    )

    # Plot text subplot
    ax4 = fig_jpeg.add_subplot(2, 2, 4)
    plt.text(
        0.15,
        0.95,
        text,
        horizontalalignment='left',
        verticalalignment='top',
        size=6,
        color='white',
    )
    plt.axis('off')
    # Adjust whitespace
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    



# this function displays the nifti, reads the keys and changes the displayed image.
# if a not-arrow-key is pressed by the user, the program exits this function
def display_nifti():

    # selects middle slices as default vaulues for the koordinates 
    x = int(nifti_data.shape[0]/2)
    y = int(nifti_data.shape[1]/2)
    z = int(nifti_data.shape[2]/2)

    # create, open and show nifti in terminal
    while( True ):

        # clear the display, so the image is on top of terminal
        os.system("clear")

        # create a jpg from this koordinates of the nifti
        create_plot( [ x, y, z ] )
        plt.savefig( tmp_nifti_file_name )

        #read jpg, display it, close it
        s = BytesIO()
        image = Image.open(tmp_nifti_file_name)
        width, height = image.size
        data = image.tobytes()
        output = sixel_output_new(lambda data, s: s.write(data), s)
        dither = sixel_dither_new(256)
        sixel_dither_initialize(dither, data, width, height, SIXEL_PIXELFORMAT_RGB888)
        sixel_encode(data, width, height, 1, dither, output)
        print(s.getvalue().decode('ascii'))
        image.close()

        # wait for user to press a key. For arrows, change displayed slice.
        # "enter"-key exit the function
        key = getkey()
        if key == keys.UP:
            x = x + 10
        elif key == keys.DOWN:
            x = x - 10
        elif key == 's':
            y = y + 10
        elif key == 'x':
            y = y - 10
        elif key == keys.LEFT:
            z = z + 10
        elif key == keys.RIGHT:
            z = z - 10
        else:
            return



# the mainfunction of the niiview-tool
def main():
    #### parse arguments from terminal ####
    parser = argparse.ArgumentParser(description="Generate a nifti image in the terminal.")
    parser.add_argument("nifti_file")
    parser.add_argument("--dpi", metavar="N", type=int, help="resolution for plotting (default: 150).", default=150)
    parser.add_argument("--show", metavar="N", type=str, help="coordinates that will be plotted", default="50,50,50")
    args = parser.parse_args()

    #### set global vars ####
    global nifti_image, nifti_data, tmp_nifti_file_name, dpi
    # Try to load the nifti-data from arguments and check for errors
    nifti_image = nb.load( args.nifti_file )
    # get 3D-image (first time point) in case of 4D-input
    if nifti_image.header['dim'][0] == 3:
        nifti_data = nifti_image.get_data()
    elif nifti_image.header['dim'][0] == 4:
        nifti_data = nifti_image.get_data()[:, :, :, 0]
    # name of a temporary jpg-file where data is written into, so libsixel can read it
    tmp_nifti_file_name = ".nifti.jpg"
    # size of nifti in terminal
    dpi=args.dpi
    # Disable Toolbar for plots
    plt.rcParams['toolbar'] = 'None'
    # Set rounding
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    # Set NAN-values to 0
    nifti_data[np.isnan(nifti_data)] = 0
    # Black background
    plt.style.use('dark_background')

    #### open/show the image ####
    display_nifti()



# standard call
if __name__ == '__main__':
    main()

