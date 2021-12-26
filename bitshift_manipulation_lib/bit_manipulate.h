#pragma once

#define bit_manip __declspec(dllexport)

#include <math.h>
#include <stdio.h>

//
extern "C" {
	__declspec(dllexport) void simple_bitwise_encode(uint8_t* imageBottom, int32_t *imageBottomShape, uint8_t* imageJoin, int32_t *imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes);
}

extern "C" {
	__declspec(dllexport) void simple_bitwise_decode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* joinedImage, int32_t* joinedImageShape, int32_t unusedBits, uint8_t numBitPlanes);
}

extern "C" {
	__declspec(dllexport) void seeded_bitwise_encode(uint8_t* imageBottom, int32_t* imageBottomShape, uint8_t* imageJoin, int32_t* imageJoinShape, int32_t unusedBits, uint8_t numBitPlanes, uint64_t *pixelPermLocs);
}


