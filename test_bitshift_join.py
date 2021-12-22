from bitshift_join import bitshift_join 
import cv2 
import numpy as np 


bits = 5
#[imgEncode, unusedBits] = bitshift_join.simple_bitwise_8X1_encode("top_small_test.png", "bottom_small_test.png")
[imgEncode, seedKey] = bitshift_join.seeded_bitwise_8X1_encode("test_join_top.png", "test_join_bottom.png")
print("seed", seedKey)
cv2.imwrite("D:\stegonography\joined_image.png", imgEncode)
cv2.imshow("encoded", imgEncode)
cv2.waitKey(0)
decodeBitshift = bitshift_join.simple_pixelwise_1X1_decode("D:\stegonography\joined_image.png", 7)
cv2.imshow("bit shift 7", decodeBitshift[1])
cv2.waitKey(0)
#cv2.imwrite("D:\stegonography\\bitshift_encode.png", decodeBitshift[1])
imgsDecode = bitshift_join.seeded_bitwise_8X1_decode("D:\stegonography\joined_image.png", seedKey)
#print(imgsDecode[1])
cv2.imwrite("D:\stegonography\\bottom_img_decode.png", imgsDecode[1])
cv2.imshow("decoded", imgsDecode[1])
cv2.waitKey(0)
#[imgEncode, seed] = bitshift_join.seeded_pixelwise_1X1_encode("test_join_top.png", "test_join_bottom.png", 7)
#cv2.imwrite("D:\stegonography\joined_image.png", imgEncode)
#print(seed)
#for i in range(0, 8):
#    imgsDecoded = bitshift_join.simple_pixelwise_1X1_decode("D:\stegonography\joined_image.png", i)
#    imgsDecoded[1] = cv2.resize(imgsDecoded[1], [800, 600])
#    cv2.imshow('Original RGB', imgsDecoded[1])
#    cv2.waitKey(0)
#for i in range(0, 8):
#    imgsDecoded = bitshift_join.seeded_pixelwise_1X1_decode("D:\stegonography\joined_image.png", i, seed)
#    imgsDecoded[1] = cv2.resize(imgsDecoded[1], [800, 600])
#    cv2.imshow('Original RGB', imgsDecoded[1])
#    cv2.waitKey(0)

#bits = 5
#imgEncode = bitshift_join.simple1X1_encode("test_join_top.png", "test_join_bottom.png", 7)
#cv2.imwrite("D:\stegonography\joined_image.png", imgEncode)
#for i in range(0, 8):
#    imgsDecoded = bitshift_join.simple1X1_decode("D:\stegonography\joined_image.png", i)
#    imgsDecoded[1] = cv2.resize(imgsDecoded[1], [800, 600])
#    cv2.imshow('Original RGB', imgsDecoded[1])
#    cv2.waitKey(0)

#print(bitshift_join.seedKeyExtract("1a6c565a7a"))
#values = [500, 800, 2]
#for i in range(0, 10000):
#    code = bitshift_join.seedKeyGen([values[0], values[1], 3], values[2])
#    decode = bitshift_join.seedKeyExtract(code)
#    if decode[0] > values[2]-1 or decode[1] > values[0] or decode[1] > values[1]:
#        print("wrong", decode, code)
#    else:
#        print(code, decode)
#print(bitshift_join.seedKeyGen([565, 787, 3], 0))