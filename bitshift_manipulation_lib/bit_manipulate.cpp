#include "pch.h"
#include <utility>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include "bit_manipulate.h"

void seeded_pixelwise_encode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* imageJoin, int32_t* imageJoinShape, uint64_t* pixelPermLocs) {
    const int64_t joinShapeFull = ((int64_t)imageJoinShape[0] * (int64_t)imageJoinShape[1]);
    const int64_t loopMax = (joinShapeFull);
    for (int64_t i = 0; i < loopMax; i += 1) {
        for (short bgr = 0; bgr < 3; bgr++) {
            imageJoin[pixelPermLocs[i]*3 + bgr] += imageBottom[i*3 + bgr];
        }
    }
}

void seeded_pixelwise_decode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* imageJoin, int32_t* imageJoinShape, uint64_t* pixelPermLocs) {
    const int64_t joinShapeFull = ((int64_t)imageJoinShape[0] * (int64_t)imageJoinShape[1]);
    const int64_t loopMax = (joinShapeFull);
    for (int64_t i = 0; i < loopMax; i += 1) {
        for (short bgr = 0; bgr < 3; bgr++) {
            imageJoin[i*3 + bgr] += imageBottom[pixelPermLocs[i] * 3 + bgr];
        }
    }

}
 
void simple_bitwise_encode(uint8_t *imageBottom, int32_t *imageBottomShape, uint8_t *imageJoin, int32_t *imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes) {
    const int64_t joinShapeFull = ((int64_t)imageJoinShape[0] * (int64_t)imageJoinShape[1]) * 3;
    const int64_t loopMax = (joinShapeFull * ((int64_t)numBitPlanes));
    int64_t currPixel = 0;
    int8_t currBit = 0;
    for (int64_t i = ((int64_t)unusedBits)*3; i < loopMax; i+=3) {
            for (short bgr = 0; bgr < 3; bgr++) {
                imageJoin[(i % joinShapeFull) + bgr] += (((imageBottom[currPixel + bgr] & (1 << currBit)) >> currBit) << (i / joinShapeFull));
            }
            currBit++;
            if (currBit > 7) {
                currBit = 0;
                currPixel +=3;
            }
        }
    //return loopMax;

}

void simple_bitwise_decode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* joinedImage, int32_t* joinedImageShape, int32_t unusedBits, uint8_t numBitPlanes) {
    const int64_t joinShapeFull = ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1]) * 3;
    int64_t loopMax = joinShapeFull * ((int64_t)numBitPlanes);
    int64_t currPixel = 0;
    int8_t currBit = 0;
    for (int64_t i = ((int64_t)unusedBits)*3; i < loopMax; i += 3) {
        int64_t currNumBitPlane = (int64_t)((i / ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1] * 3)));
        for (short bgr = 0; bgr < 3; bgr++) {
            imageBottom[currPixel + bgr] |= ((joinedImage[(i % ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1] * 3)) + bgr] & (1<<currNumBitPlane)) >> currNumBitPlane) << currBit;
 
        }
        currBit++;
        if (currBit > 7) {
            currBit = 0;
            currPixel += 3;
        }
    }

}

void seeded_bitwise_encode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* imageJoin, int32_t* imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes, uint64_t* pixelPermLocs) {
    const int64_t joinShapeFull = ((int64_t)imageJoinShape[0] * (int64_t)imageJoinShape[1]);
    const int64_t loopMax = (((int64_t)imageJoinShape[0] * (int64_t)imageJoinShape[1]) * ((int64_t)numBitPlanes));
    int64_t currPixel = 0;
    int8_t currBit = 0;
    for (int64_t i = unusedBits; i < loopMax; i += 1) {
        for (short bgr = 0; bgr < 3; bgr++) {
            imageJoin[(pixelPermLocs[i] % joinShapeFull) * 3 + bgr] += (((imageBottom[currPixel + bgr] & (1 << currBit)) >> currBit) << (pixelPermLocs[i] / (joinShapeFull)));
        }
        currBit++;
        if (currBit > 7) {
            currBit = 0;
            currPixel += 3;
        }
    }

}

void seeded_bitwise_decode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* joinedImage, int32_t* joinedImageShape, int32_t unusedBits, uint8_t numBitPlanes, uint64_t* pixelPermLocs) {

    const int64_t joinShapeFull = ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1]);
    const int64_t loopMax = (((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1]) * ((int64_t)numBitPlanes));
    int64_t currPixel = 0;
    int8_t currBit = 0;
    for (int64_t i = unusedBits; i < loopMax; i += 1) {
        for (short bgr = 0; bgr < 3; bgr++) {
            int64_t currNumBitPlane = (int64_t)((pixelPermLocs[i] / ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1])));
            imageBottom[currPixel + bgr] |= ((joinedImage[(pixelPermLocs[i] % ((int64_t)joinedImageShape[0] * (int64_t)joinedImageShape[1]))*3 + bgr] & (1 << currNumBitPlane)) >> currNumBitPlane) << currBit;
            //imageJoin[(pixelPermLocs[i] % joinShapeFull) * 3 + bgr] += (((imageBottom[currPixel + bgr] & (1 << currBit)) >> currBit) << (pixelPermLocs[i] / (joinShapeFull)));
        }
        currBit++;
        if (currBit > 7) {
            currBit = 0;
            currPixel += 3;
        }
    }

}

