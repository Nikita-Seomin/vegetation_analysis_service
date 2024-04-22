
import zipfile
import rasterio
import uuid
import os
import numpy as np


def getPathToTrueColorFromZip(zipFilePath):
    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile

    for c in z.namelist():
        if 'True_color' in c:
            tr = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")

            # Reading true_image band
            trueArray = tr.read()
            metadata = tr.meta.copy()
            metadata['photometric'] = "RGB"
            tr.close()

            # post true color
            path = os.path.join('./data/true_colors/', str(uuid.uuid4()) + ".tiff")
            with rasterio.open(path, "w", **metadata) as dst:
                # Write RGB bands to the file
                dst.write(trueArray)
                dst.close()
            return path

    return None


def getPathToRedFromZip(zipFilePath):
    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile

    isTrue  = False
    for c in z.namelist():
        if 'B04' in c:
            isTrue = True
            red = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")

    # Reading true_image band
    if isTrue:
        redArray = red.read()
        metadata = red.meta.copy()

    # post true color
    path = os.path.join('./data/B04/', str(uuid.uuid4()) + ".tiff")
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(redArray)

    return path


def getPathToNirFromZip(zipFilePath):
    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile

    isTrue  = False
    for c in z.namelist():
        if 'B08' in c:
            isTrue = True
            nir = rasterio.open('zip+file:./' + zipFilePath + '/' + c, "r")

    # Reading true_image band
    if isTrue:
        nirArray = nir.read()
        metadata = nir.meta.copy()

    # post true color
    path = os.path.join('./data/B08/', str(uuid.uuid4()) + ".tiff")
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(nirArray)

    return path

