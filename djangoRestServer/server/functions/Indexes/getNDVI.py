# NDVI Python Script
#
# GNU GENERAL PUBLIC LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Created by Alexandros Falagas
# Last update 13-09-2022

import os
import optparse
import numpy as np
import rasterio
import zipfile
import uuid


import matplotlib.pyplot as plt
import rasterio as rio
from rasterio import plot
import detectree as dtr
from PIL import Image

class OptionParser(optparse.OptionParser):
    "A class to parse the arguments."

    def check_required(self, opt):
        "A simple method to check the required parameters."

        option = self.get_option(opt)
        # Assumes the option's 'default' is set to None!
        if getattr(self.values, option.dest) is None:
            self.error("{} option is required.".format(option))


def getNDVI(r: np.array, n: np.array) -> np.array:
    """The NDVI function.

    Args:
        r (np.array): Red band array
        n (np.array): NIR band array

    Returns:
        np.array: NDVI array
    """
    np.seterr(divide='ignore', invalid='ignore')  # Ignore the divided by zero or Nan appears
    # BE CAREFULL! Without this convertion, doesn't work correctly !
    n = n.astype(rasterio.float32)
    r = r.astype(rasterio.float32)
    ndvi = (n - r) / (n + r)  # The NDVI formula

    return ndvi

#function create ndvi and craete the mask using it and build the tiff with cutting trees
def NDVI(zipFilePath):

    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile
    for c in z.namelist():

        print(c)
        if 'B04' in c:
            red = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        elif 'B08' in c:
            nir = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        else:
            tr = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")



    # Reading red band.
    redArray = red.read()
    # Copy metadata
    metadata = tr.meta.copy()

    # Reading NIR band
    nirArray = nir.read()

    # Reading true_image band

    true_array = tr.read()
    from rasterio.enums import ColorInterp



    red.close()
    nir.close()
    tr.close()
    print(true_array)

    def rescale(arr):
        arr_min = arr.min()
        arr_max = arr.max()
        return (arr - arr_min) / (arr_max - arr_min)

    # red_arr_b = 255.0 * rescale(true_array[0])
    # green_arr_b = 255.0 * rescale(true_array[1])
    # blue_arr_b = 255.0 * rescale(true_array[2])




    # Calling the NDVI function.
    ndviArray = getNDVI(redArray, nirArray)
    print(ndviArray[0][0])
    for str_image in range(true_array.shape[1]):
        for pixel in range(true_array.shape[2]):
            if ndviArray[0][str_image][pixel] <= -0.5:
                true_array[0][str_image][pixel] = 51
                true_array[1][str_image][pixel] = 153
                true_array[2][str_image][pixel] = 255

            if ndviArray[0][str_image][pixel] <= 0:
                true_array[0][str_image][pixel] = 151
                true_array[1][str_image][pixel] = 151
                true_array[2][str_image][pixel] = 151

            elif ndviArray[0][str_image][pixel] <= .033:
                true_array[0][str_image][pixel] = 255
                true_array[1][str_image][pixel] = 255
                true_array[2][str_image][pixel] = 255

            elif ndviArray[0][str_image][pixel] <= .066:
                true_array[0][str_image][pixel] = 196
                true_array[1][str_image][pixel] = 184
                true_array[2][str_image][pixel] = 168

            elif ndviArray[0][str_image][pixel] <= 0.05:
                true_array[0][str_image][pixel] = 180
                true_array[1][str_image][pixel] = 150
                true_array[2][str_image][pixel] = 108

            elif ndviArray[0][str_image][pixel] <= .133:
                true_array[0][str_image][pixel] = 164
                true_array[1][str_image][pixel] = 130
                true_array[2][str_image][pixel] = 76

            elif ndviArray[0][str_image][pixel] <= .166:
                true_array[0][str_image][pixel] = 148
                true_array[1][str_image][pixel] = 114
                true_array[2][str_image][pixel] = 60

            elif ndviArray[0][str_image][pixel] <= .2:
                true_array[0][str_image][pixel] = 124
                true_array[1][str_image][pixel] = 158
                true_array[2][str_image][pixel] = 44

            elif ndviArray[0][str_image][pixel] <= .25:
                true_array[0][str_image][pixel] = 148
                true_array[1][str_image][pixel] = 182
                true_array[2][str_image][pixel] = 20

            elif ndviArray[0][str_image][pixel] <= .3:
                true_array[0][str_image][pixel] = 116
                true_array[1][str_image][pixel] = 170
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .35:
                true_array[0][str_image][pixel] = 100
                true_array[1][str_image][pixel] = 162
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .4:
                true_array[0][str_image][pixel] = 84
                true_array[1][str_image][pixel] = 150
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .45:
                true_array[0][str_image][pixel] = 60
                true_array[1][str_image][pixel] = 134
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .5:
                true_array[0][str_image][pixel] = 28
                true_array[1][str_image][pixel] = 114
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .6:
                true_array[0][str_image][pixel] = 4
                true_array[1][str_image][pixel] = 96
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .7:
                true_array[0][str_image][pixel] = 4
                true_array[1][str_image][pixel] = 74
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .8:
                true_array[0][str_image][pixel] = 4
                true_array[1][str_image][pixel] = 56
                true_array[2][str_image][pixel] = 4

            elif ndviArray[0][str_image][pixel] <= .9:
                true_array[0][str_image][pixel] = 4
                true_array[1][str_image][pixel] = 40
                true_array[2][str_image][pixel] = 4
            else:
                true_array[0][str_image][pixel] = 0
                true_array[1][str_image][pixel] = 0
                true_array[2][str_image][pixel] = 0

    # true_array[0] = 255.0 * rescale(true_array[0])
    # true_array[1] = 255.0 * rescale(true_array[1])
    # true_array[2] = 255.0 * rescale(true_array[2])

    # print(ndviArray([[np.array(ndviArray[0][0])*3]]))

    #create mask from ndvi
    # ndviArray[ndviArray > .6] = 1
    # ndviArray[ndviArray < .6] = 0

    # print(ndviArray)
    #
    # #multiply mask and true color image for take polygons with vegetarians
    # trueMultiplyNdvi = true_array * ndviArray

    #Create path for mask tiff
    path = os.path.join('./data/result/', str(uuid.uuid4()) + ".tiff")
    # print('metadata: ',metadata)
    # Writing the NDVI raster with the same properties as the original data
    # metadata['photometric'] = "RGB"
    from rasterio.enums import ColorInterp
    metadata.update({"driver": "GTiff", "dtype": rasterio.uint8, "count": 3})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.colorinterp = [
            ColorInterp.red, ColorInterp.green, ColorInterp.blue]
        dst.write(true_array)

    #return path to file with cutting trees
    return path


