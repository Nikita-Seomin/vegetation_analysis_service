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

import sys
import os
import optparse
import numpy as np
import rasterio
import zipfile


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

def NDVI(zipFilePath):
    name = "NDVI.tiff"

    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile
    for c in z.namelist():

        # print(c)
        if c == 'B04_8.tiff':
            red = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        else:
            nir = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")

    # Reading red band.
    red_array = red.read()
    metadata = red.meta.copy()

    # Reading NIR band
    nir_array = nir.read()

    # Calling the NDVI function.
    ndvi_array = getNDVI(red_array, nir_array)

    # Updating metadata
    metadata.update({"driver": "GTiff", "dtype": rasterio.float32})

    # Writing the NDVI raster with the same properties as the original data
    with rasterio.open(os.path.join('./server/functions/', name), "w", **metadata) as dst:
        if ndvi_array.ndim == 2:
            dst.write(ndvi_array, 1)
        else:
            dst.write(ndvi_array)