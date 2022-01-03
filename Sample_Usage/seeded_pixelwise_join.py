#used to import the bitshift_join library
from os import chdir, getcwd
from sys import path
chdir("..")
currFileLoc = getcwd()
path.insert(0, currFileLoc)

from bitshift_join import bitshift_join 
import cv2 
import numpy as np 
import time 
import ctypes
import random

b_join = bitshift_join() #sets up the .dll. Needed for running the code.
front_image_path = "killer_trees.png"#put your front image's path here
back_image_path = "killer_tree_origin.png"#put your back image's path here
bits_used_by_front = 5#put the number of bits your front image will contain (your back image will have 8-bits_used_by_front bits)
joined_image_path = "joined_img_pixlwise.png"#where to place your joined image (include the image name as a .png)
decoded_image_top_path = "top_img_pxlwise.png"#where to place the top image that has been decoded
decoded_image_bottom_path = "bot_img_pxlwise.png"#where to place the bottom image that has been decoded

###Encoding section
startTime = time.time()
print("encoding...")
[imgEncoded, seedKey] = b_join.seeded_pixelwise_1X1_encode(front_image_path, back_image_path, bits_used_by_front)
print("done encoding. Time (seconds):", time.time()-startTime)
print("Seed Key Generated:", seedKey)
cv2.imwrite(joined_image_path, imgEncoded)

##Decoding section 
startTime = time.time()
print("decoding...")
imgsDecoded = b_join.seeded_pixelwise_1X1_decode(joined_image_path, bits_used_by_front, seedKey)
print("done decoding. Time (seconds):", time.time()-startTime)
cv2.imwrite(decoded_image_top_path, imgsDecoded[0])
cv2.imwrite(decoded_image_bottom_path, imgsDecoded[1])
