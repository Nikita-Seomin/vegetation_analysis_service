import rasterio
import zipfile
import uuid
import os

from rasterio.enums import ColorInterp
from server.functions.Indexes.getColorNDVI import getNDVIArray


def GIGreen(zipFilePath):
    z = zipfile.ZipFile(zipFilePath)  # Flexibility with regard to zipfile
    for c in z.namelist():
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
    # # print(redArray)
    #
    # Reading blue band.
    blueArray = blue.read()

    # Copy metadata
    metadata = tr.meta.copy()

    # Reading nir band
    nirArray = nir.read()
    # print(nirArray)

    # Reading tr band
    trArray = tr.read()

    metadata['photometric'] = "RGB"

    # ndviArray = getNDVIArray(redArray, nirArray)
    #
    # ndviArray[ndviArray >= .5] = 1
    # ndviArray[ndviArray < .1] = 0

    GIGreenImageArray = nirArray / greenArray

    for str_image in range(trArray.shape[1]):
        for pixel in range(trArray.shape[2]):
            if GIGreenImageArray[0][str_image][pixel] > 7:
                trArray[0][str_image][pixel] = 134
                trArray[1][str_image][pixel] = 255
                trArray[2][str_image][pixel] = 170
            elif GIGreenImageArray[0][str_image][pixel] > 5:
                trArray[0][str_image][pixel] = 54
                trArray[1][str_image][pixel] = 250
                trArray[2][str_image][pixel] = 113
            elif GIGreenImageArray[0][str_image][pixel] > 3:
                trArray[0][str_image][pixel] = 0
                trArray[1][str_image][pixel] = 196
                trArray[2][str_image][pixel] = 59
            elif GIGreenImageArray[0][str_image][pixel] > 2:
                trArray[0][str_image][pixel] = 0
                trArray[1][str_image][pixel] = 118
                trArray[2][str_image][pixel] = 35
            else :
                trArray[0][str_image][pixel] = 0
                trArray[1][str_image][pixel] = 0
                trArray[2][str_image][pixel] = 0

    GIGreenImageArray[GIGreenImageArray >= 5] = 100
    GIGreenImageArray[GIGreenImageArray < 5] = 0



    # for str_image in range(trArray.shape[1]):
    #     for pixel in range(trArray.shape[2]):
    #         if .04 < GIGreenImageArray[0][str_image][pixel] < .1:
    #             trArray[0][str_image][pixel] = 255
    #             trArray[1][str_image][pixel] = 0
    #             trArray[2][str_image][pixel] = 0

    path = os.path.join('./data/GIGreen/', str(uuid.uuid4()) + ".tiff")

    metadata.update({"driver": "GTiff", "dtype": rasterio.uint8})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.colorinterp = [
            ColorInterp.red, ColorInterp.green, ColorInterp.blue]
        dst.write(trArray)

    # return path to file with cutting trees
    return path
