import os
import uuid
import zipfile

import numpy as np
import rasterio


def getNDVIArray(r: np.array, n: np.array) -> np.array:
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


def getNDVI(zipFilePath):

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
    ndviArray = getNDVIArray(redArray, nirArray)
    print(true_array.shape)

    #Create path for mask tiff
    path = os.path.join('./data/result/', str(uuid.uuid4()) + ".tiff")
    # print('metadata: ',metadata)
    # Writing the NDVI raster with the same properties as the original data
    # metadata['photometric'] = "RGB"
    from rasterio.enums import ColorInterp
    metadata.update({"driver": "GTiff", "dtype": rasterio.float32})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(ndviArray)

    #return path to file with cutting trees
    return path