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
    metadata = red.meta.copy()

    # Reading NIR band
    nirArray = nir.read()

    # Reading true_image band
    true_array = tr.read()

    red.close()
    nir.close()
    tr.close()


    # Calling the NDVI function.
    ndviArray = getNDVI(redArray, nirArray)


    #create mask from ndvi
    ndviArray[ndviArray > .6] = 1
    ndviArray[ndviArray < .6] = 0

    print(ndviArray)
    #
    # #multiply mask and true color image for take polygons with vegetarians
    # trueMultiplyNdvi = true_array * ndviArray

    #Create path for mask tiff
    path = os.path.join('./data/result/', str(uuid.uuid4()) + ".tiff")
    print('metadata: ',metadata)
    # Writing the NDVI raster with the same properties as the original data
    metadata.update({"driver": "GTiff", "dtype": rasterio.float32})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(ndviArray)

    #return path to file with cutting trees
    return path

def getTreeMask(tile_filename):
    tr = rasterio.open(tile_filename, "r")
    metadata = tr.meta.copy()
    metadata['photometric'] = "RGB"

    # use the pre-trained model to segment the image into tree/non-tree-pixels
    y_pred = np.array([dtr.Classifier().predict_img(tile_filename)])

    path = os.path.join('./data/treeMasks/', str(uuid.uuid4()) + ".tiff")
    metadata.update({"driver": "GTiff", "dtype": rasterio.float32, "count": 1})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(y_pred)
        dst.close()

    return path
