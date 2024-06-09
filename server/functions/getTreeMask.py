import rasterio
import detectree as dtr
import uuid
import os
import numpy as np


def getTreeMask(tile_filename):
    print(tile_filename)
    tr = rasterio.open(tile_filename, "r")
    metadata = tr.meta.copy()
    trArray = tr.read()
    print(trArray)
    # metadata['photometric'] = "RGB"

    # use the pre-trained model to segment the image into tree/non-tree-pixels
    y_pred = np.array([dtr.Classifier().predict_img(tile_filename)])

    # y_pred[y_pred == 255] = 1

    trueMultiplyNDVI = trArray * y_pred

    path = os.path.join('./data/treeMasks/', str(uuid.uuid4()) + ".tiff")
    metadata.update({"driver": "GTiff", "dtype": rasterio.uint8, "count": 1})
    with rasterio.open(path, "w", **metadata) as dst:
        dst.write(y_pred)
        dst.close()

    return path