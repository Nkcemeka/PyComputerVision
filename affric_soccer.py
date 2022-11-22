import sys
from PIL import Image
import numpy as np
import math

if len(sys.argv)!=4:
    print("usage is: %s image_in image_out thresh"%(sys.argv[0]))
    print("        thresh is between 0 and 255")
    print("        smaller values make detection more sensitive")
    sys.exit()


pil_image_rgb = Image.open(sys.argv[1])
image_rgb = np.asarray(pil_image_rgb, np.float)
Image.fromarray(image_rgb.astype(np.uint8)).save("verify_image.jpg")

pil_image_bw = pil_image_rgb.convert('L')
pil_image_bw.show()
image_bw = np.asarray(pil_image_bw, np.float)
print(image_bw)
rows = image_bw.shape[0]
cols = image_bw.shape[1]
thresh = float(sys.argv[3])
print(f"rows = {rows}; cols = {cols}; thresh = {thresh}")

image_out = np.zeros((rows, cols), np.float)

# horizontal
for i in range(1, rows-1):
    image_out[i,1:-1] = (    (image_bw[i-1, 2:] - image_bw[i-1, :-2])   + \
                             (image_bw[i, 2:]   - image_bw[i,   :-2])*2 + \
                             (image_bw[i+1,2:]  - image_bw[i+1, :-2])) ** 2

# vertical
for j in range(1, cols-1):
    image_out[1:-1,j] += ( (image_bw[2:, j-1] - image_bw[:-2, j-1])   + \
                             (image_bw[2:, j]   - image_bw[:-2, j])*2 + \
                             (image_bw[2:, j+1]  - image_bw[:-2, j])) ** 2

image_out = np.sqrt(image_out)
maxval = np.amax(image_out)
print(f"maxval = {maxval}")
image_out = 254*image_out/maxval
image_out = np.where(image_out < thresh, 0, 255)
image_out = image_out.astype(np.uint8)
a = Image.fromarray(image_out)
a.save(sys.argv[2])
a.show()