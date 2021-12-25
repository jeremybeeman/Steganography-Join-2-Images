#include "pch.h"
#include <utility>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include "bit_manipulate.h"


void binary_combine(uint8_t *imageBottom, int32_t *imageBottomShape, uint8_t *imageJoin, int32_t *imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes) {
    const int64_t loopMax = (imageBottomShape[0]*imageBottomShape[1]) * 3* ((int64_t)numBitPlanes);
    //long frontLoc[3];
    //long backLoc[3];
    int64_t currPixel = 0;
    short currBit = 0;
    for (int64_t i = 0; i < loopMax; i+=3) {
        if (i >= unusedBits) {
            //frontLoc[0] = i % imageJoinShape[0];
            //frontLoc[1] = (i / imageJoinShape[0]) % imageJoinShape[0];
            //frontLoc[2] = (i / (imageJoinShape[0] * imageJoinShape[1]));
            //backLoc[0] = (currPixel % imageBottomShape[0]);
            //backLoc[1] = (currPixel / imageBottomShape[0]);
            for (short rgb = 0; rgb < 3; rgb++) {
                imageJoin[(i % (imageBottomShape[0] * imageBottomShape[1] * 3)) + rgb] += (((imageBottom[currPixel + rgb] & (1 << currBit)) >> currBit) << (i / (imageJoinShape[0] * imageJoinShape[1] * 3)));

                //imageJoin[frontLoc[0]][frontLoc[1]][rgb] += (((imageBottom[backLoc[0]][backLoc[1]][rgb] & (1 << currBit)) >> currBit) << frontLoc[2]);
            }
            currBit++;
            if (currBit > 7) {
                currBit = 0;
                currPixel += 3;
                //if (currPixel > imageJoinShape[0] * imageJoinShape[1] * imageJoinShape[2]) {
                //    currPixel -= 6;
                //}
            }
            //printf((char *)(imageJoin[i]));
        }
    }

}

//void binary_split(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* imageJoin, int32_t* imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes) {
//
//
//}

