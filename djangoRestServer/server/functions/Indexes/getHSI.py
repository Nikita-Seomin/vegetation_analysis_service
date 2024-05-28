import rasterio
import zipfile
import uuid
import os
import numpy as np

from server.functions.Indexes.getNDVI import getNDVI


def HSI(zipFilePath):

    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile
    for c in z.namelist():
        # print(c)
        if 'B03' in c:
            green = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        elif 'B04' in c:
            red = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        elif 'B02' in c:
            blue = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        elif 'B08' in c:
            nir = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")
        elif 'True_color' in c:
            tr = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")

    # Reading green band.
    greenArray = green.read()


    # Reading red band.
    redArray = red.read()
    # print(redArray)

    # Reading blue band.
    blueArray = blue.read()
    # print(blueArray)

    # Copy metadata
    metadata = nir.meta.copy()


    # Reading nir band
    nirArray = nir.read()
    # print(nirArray)

    # Reading tr band
    trArray = tr.read()

    ndviArray = getNDVI(redArray, nirArray)

    ndviArray[ndviArray >= .1] = 1
    ndviArray[ndviArray < .1] = 0

    hsiImageArray = (nirArray / np.abs(greenArray - blueArray)) * ndviArray
    print(hsiImageArray)

    hsiImageArray[hsiImageArray >= 15] = 100
    hsiImageArray[hsiImageArray < 15] = 0

    path = os.path.join('./data/hsi/', str(uuid.uuid4()) + ".tiff")



    metadata.update({"driver": "GTiff", "dtype": rasterio.uint8, "count": 1})
    with rasterio.open(path, "w", **metadata) as dst:
        # dst.colorinterp = [
        #     ColorInterp.red, ColorInterp.green, ColorInterp.blue]
        dst.write(hsiImageArray)

    # return path to file with cutting trees
    return path
