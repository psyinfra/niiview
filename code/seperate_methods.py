#!/home/tkadelka/env/niicat_env/bin/python3

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nb
import time

from getkey import getkey, keys

from libsixel import *
from PIL import Image
from io import BytesIO

# This function creates the figure, that should be plotted later.
# It is based on: _plot_nifti_preview(iFile, show, return_fig=False, dpi=150)
# from https://github.com/vnckppl/niipre"""

'''    plt.text(-10, mY + 5, oL, fontsize=9, color='red')  # Label on left side

    # Textual information
    # sform code
    sform = np.round(image.get_sform(), decimals=2)
    sform_txt = str(sform).replace('[', ' ').replace(']', ' ').replace(' ', '   ').replace('   -', '  -')

    # qform code
    qform = np.round(image.get_qform(), decimals=2)
    qform_txt = str(qform).replace('[', ' ').replace(']', ' ').replace(' ', '   ').replace('   -', '  -')

    # Dimensions
    dims = str(data.shape).replace(', ', ' x ').replace('(', '').replace(')', '')
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
    type = image.header.get_data_dtype()
    type_str = ("Data type: " + str(type))

    # Volumes
    volumes = ("Volumes: " + str(image.header['dim'][4]))

    # Range
    min = np.round(np.amin(data), decimals=2)
    max = np.round(np.amax(data), decimals=2)
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
    ax4 = fig.add_subplot(2, 2, 4)
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
    '''


def init_plot(iFile, show=""):

    # Disable Toolbar for plots
    plt.rcParams['toolbar'] = 'None'

    # Set rounding
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

    # Load data
    image = nb.load(iFile)

    # 3D data
    if image.header['dim'][0] == 3:
        data = image.get_data()
        # 4D data
    elif image.header['dim'][0] == 4:
        data = image.get_data()[:, :, :, 0]

    # Header
    header = image.header

    # Set NAN to 0
    data[np.isnan(data)] = 0

    # Spacing for Aspect Ratio
    sX = header['pixdim'][1]
    sY = header['pixdim'][2]
    sZ = header['pixdim'][3]

    # Size per slice
    lX = data.shape[0]
    lY = data.shape[1]
    lZ = data.shape[2]

    # Middle slice number as default
    mX = int(lX / 2)
    mY = int(lY / 2)
    mZ = int(lZ / 2)
    # if show is set, don't use the default slice
    if len( show.split(",") ) == 3:	
        requested = show.split(",")
        mX = int(requested[0])
        mY = int(requested[1])
        mZ = int(requested[2])


    # Middle slice number

    # True middle point
    tmX = lX / 2.0
    tmY = lY / 2.0
    tmZ = lZ / 2.0

    # Orientation
    qfX = image.get_qform()[0, 0]
    sfX = image.get_sform()[0, 0]

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

    # This gives different results
    # oL = nb.aff2axcodes(image.affine)[0]


    # Plot main window
    fig = plt.figure(
        facecolor='black',
        figsize=(5, 4)
    )

    # Black background
    plt.style.use('dark_background')

    # Coronal
    ax1 = fig.add_subplot(2, 2, 1)
    imgplot = plt.imshow(
        np.rot90(data[:, mY, :]),
        aspect=sZ / sX,
    )
    imgplot.set_cmap('gray')

    ax1.hlines(tmZ, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax1.vlines(tmX, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')

    # Sagittal
    ax2 = fig.add_subplot(2, 2, 2)
    imgplot = plt.imshow(
        np.rot90(data[mX, :, :]),
        aspect=sZ / sY,
    )
    imgplot.set_cmap('gray')

    ax2.hlines(tmZ, 0, lY, colors='red', linestyles='dotted', linewidth=.5)
    ax2.vlines(tmY, 0, lZ, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')

    # Axial
    ax3 = fig.add_subplot(2, 2, 3)
    imgplot = plt.imshow(
        np.rot90(data[:, :, mZ]),
        aspect=sY / sX
    )
    imgplot.set_cmap('gray')

    ax3.hlines(tmY, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax3.vlines(tmX, 0, lY, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')
    plt.savefig( tmp_nifti_file )


def change_plot_coronal( axis_shift ):
    fig = plt.figure(
        facecolor='black',
        figsize=(5, 4)
    )
    # Axial
    ax3 = fig.add_subplot(2, 2, 3)
    imgplot = plt.imshow(1)
    imgplot.set_cmap('gray')

    ax3.hlines(tmY, 0, lX, colors='red', linestyles='dotted', linewidth=.5)
    ax3.vlines(tmX, 0, lY, colors='red', linestyles='dotted', linewidth=.5)

    plt.axis('off')
    plt.savefig( tmp_nifti_file )


# the mainfunction of the nii-viewer-tool
def main():

    global data, xyz, tmp_nifti_file

    # parse arguments from terminal
    parser = argparse.ArgumentParser(description="Generate previews of nifti image on the terminal.")
    parser.add_argument("nifti_file")
    parser.add_argument("--dpi", metavar="N", type=int, help="resolution for plotting (default: 150).", default=150)
    parser.add_argument("--show", metavar="N", type=str, help="coordinates that will be plotted", default="50,50,50")
    args = parser.parse_args()

    # where the data is written to, so libsixel can read it
    tmp_nifti_file = "nifti.jpg"

    # will be set to False later (in case of invalid key)
    run_prog = True
    slices = args.show.split(",")


    
    xyz = [int(slices[0]), int(slices[1]), int(slices[2])]






    show_this_slices = str(xyz[0]) + "," + str(xyz[1]) + "," + str(xyz[2])
    init_plot( args.nifti_file, show_this_slices )
    
    s = BytesIO()
    image_data = Image.open(tmp_nifti_file)
    width, height = image_data.size
    data = image_data.tobytes()
    output = sixel_output_new(lambda data, s: s.write(data), s)
    dither = sixel_dither_new(256)
    sixel_dither_initialize(dither, data, width, height, SIXEL_PIXELFORMAT_RGB888)
    sixel_encode(data, width, height, 1, dither, output)
    print(s.getvalue().decode('ascii'))
    image_data.close()


    while( run_prog == True ):

        key = getkey()
        if key == keys.UP:
            change_plot_coronal( 10 )
        elif key == keys.DOWN:
            xyz[0] = xyz[0] - 10
        elif key == 's':
            xyz[1] = xyz[1] + 10
        elif key == 'x':
            xyz[1] = xyz[1] - 10
        elif key == keys.LEFT:
            xyz[2] = xyz[2] + 10
        elif key == keys.RIGHT:
            xyz[2] = xyz[2] - 10
        else:
            run_prog = False


        s = BytesIO()
        image_data = Image.open(tmp_nifti_file)
        width, height = image_data.size
        data = image_data.tobytes()
        output = sixel_output_new(lambda data, s: s.write(data), s)
        dither = sixel_dither_new(256)
        sixel_dither_initialize(dither, data, width, height, SIXEL_PIXELFORMAT_RGB888)
        sixel_encode(data, width, height, 1, dither, output)
        print(s.getvalue().decode('ascii'))
        image_data.close()

        
   

if __name__ == '__main__':
    main()

