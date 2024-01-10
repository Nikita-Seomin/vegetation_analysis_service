from PIL import Image
import numpy

im1 = Image.open('input/B08.tiff')
im2 = Image.open('input/B04.tiff')
# im.show()
imarray1 = numpy.array(im1)
imarray2 = numpy.array(im2)
# print(imarray.shape)
# print(im1.size)
# print(imarray1)
imRes1 = numpy.array([])
# print(imarray1.size)
# print(imarray1)
# print()
# print(imarray2)
# print()
# print(numpy.multiply(imarray1,imarray2))
# print(imarray1[1])
for i in range(len(imarray1)):
    temp_list = (numpy.subtract(imarray1[i], imarray2[i]))
    print(temp_list)
    imRes1 = numpy.append(imRes1, temp_list, axis=0)


print(imRes1)
# imRes1.save("filename.tiff", format="TIFF", save_all=True)
new_im = Image.fromarray(imRes1.astype('uint8'))
new_im.show()