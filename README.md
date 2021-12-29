# Steganography-Join-2-Images

![Pixelwise Example Image](https://github.com/jeremybeeman/Steganography-Join-2-Images/blob/main/README_images/pixelwise_example.png)

This repo focuses on joining two images together via different means. This repo contains a library that joins a top image with a bottom image. The different joins have tradeoffs. 
## Table of Contents 
- [Summary](#summary)
   * [Uses](#uses)
   * [Required Software](#required-software)
   * [Python Used Modules](#python-used-modules)
- [Before Starting](#notes)
- [Definition of Main Terms](#definitions)
   * [Terms](#terms)
   * [Seed Key Guide](#seed-key-guide)
- [Test Calculations Website](#test-calculations)
- [Options (Naming Conventions)](#options)
  * [Data Accessibility Options](#data-accessibility-options)
  * [Data to Encode Options](#data-to-encode-options)
  * [Size Indication Options](#size-indication-options)

## Summary 

This repository combines two images together using various methods of encoding. The method for combining these images together has to do with the fact that images tend to be stored as an unsigned integer. It also relies on that human eyes tend to not respond to very low level brightness differences (that is, the difference between brightness 2 and brightness 1). So, a bottom image can be encoded into the top image's bottom bits. There are two methods to this encoding: pixelwise and bitwise. Pixelwise uses the pixels of the bottom image and combines them with the top image's pixels. This causes the bottom image's colors to be muted in comparison to the original. If preserving the color/brightness of the bottom image, then bitwise encoding is key. This places the brightness levels of the bottom image into the pixels of the top image, instead of the pixel values themselves. This preservesthe color/brightness, but not the original size of the image. 

### Uses 

- Making NFTs more hardened to right-clicking (one can't access the second image without a code). 
- Making ARGs that are tougher to crack. 
- Other ideas you might have...

### Required Software 

| Software                               | Version (or Comparable)  |
|:--------------------------------------:|:------------------------:|
| Python                                 | 3.9.9                    |
| numpy                                  | 1.20.3                   |
| opencv-contrib-python                  | 4.5.4.60                 |    
| Visual Studio                          | 2019 (16.10.3)           | 

### Python Used Modules 

| Module                                 | Usage  |
|:--------------------------------------:|:------------------------:|
| cv2                                    | For loading images for processing                                                                     |
| numpy                                  | ctypes integration, random permutations                                                               |
| math                                   | sqrt for determining width/height of bitwise operations                                               |
| random                                 | For generating the random seed used to encode/decode pixelwise and bitwise operations                 |   
| ctypes                                 | For interfacing with C++ .dll                                                                         |

## Notes 

- All images MUST be stored as .png instead of .jpeg or .jpg. This is because JPEGs are lossy, and will filter out these encoding methods, as these methods tend to be high frequency. 
- The two images are forced to be the same size before combining occurs. It is recommended that the images are resized before using this program. That way the desired aspect respect ratios can be perserved. 
- This library cannot interface with any transparent images. There must be a background to the image for this system.
- This is a WINDOWS library right now, due to the .dll extension.

## Definitions

### Terms

**Bit Planes/Layers:** Name for a specific bit of an image. All 8-bit images have 8 bit planes. The lowest significant bit is the lowest bit plane. The most significant bit is the highest bit plane. When there's talk of multiple bit planes being used, the count starts at the lowest significant bit and goes up 1 bit plane at a time. 

**Pixelwise Encoding/Decoding:** Where the bottom image's pixels are placed in directly on top of the top image's bottom bits. This preserves the original size of the bottom image, but degrades the original colors.

| ![Pixelwise Example Image](https://github.com/jeremybeeman/Steganography-Join-2-Images/blob/main/README_images/pixelwise_example.png) |
|:---:|
| **Pixelwise Encoding Example. The encoding level done on this image involved 5 bits of the front image and 3 bits for the bottom image, limiting the bottom image's brightness values.**

**Bitwise Encoding/Decoding:** Where the bottom image's pixels are broken up into their 8-bit brightness levels and then recombined during the decoding phase. This preserves all of the brightness values of hte original image. However, the image must be shrunk to have its data fit within the original image.

| ![Bitwise Example Image](https://github.com/jeremybeeman/Steganography-Join-2-Images/blob/main/README_images/bitwise_example.png) |
|:---:|
| **Bitwise Encoding Example. This example shows the bottom bit layer of the image. A pixel of the top image associates to a bit from the bottom image, perserving original brightness but decreasing size**|

**Simple:** All of the pixels or bits of the bottom image aren't scrambled using a seed key. There is no need for a seed key, as the data is arranged in a direct manner (NOTE: while the data may not be scrambled, there might need to be some data available to decode the image. Simple just means all the bitwise/pixelwise data is placed in a linear fashion, and there's not any jumping around of bits/pixels). 

**Seeded:** All of the pixels or bits of the bottom image are scrambled around using a seed key. Without the seed key, it is very hard to extract the bottom image easily. 

### Seed Key Guide

For the seed key, each component serves a purpose. In a seed, a number is followed by a lowercase letter. In order to unravel the values, the number is multiplied by the letter where a=1 and z=26. The seed will look slightly different between pixelwise and bitwise operations. For the seed keys, the values are as follows:
1. Bit Plane Layer to start at (starting at 0 and going up from there). 
2. Height Seed Start to start where the scramble occurs. 
3. Width Seed Start to start where the scramble occurs. 
4. Unused Pixels of Top Image to denote how many unused pixels are there. Used for padding in bitwise operations when the bottom image can't fit within all of the pixels and perserve its aspect ratio. 
5. Height of bottom image to denote the shape of the bottom image. 
6. Width of bottom image to denote the shape of the bottom image. 
7. Number of bit planes used to denote how many bit planes are possible to be decoded. Mainly used for bitwise operations. 

All pixelwise operations have 0 unused pixels and a 1a for the number of bit planes used. 

| ![Seed Key Guide](https://github.com/jeremybeeman/Steganography-Join-2-Images/blob/main/README_images/seed_key.png) |
|:---:|
| Guide to the parts of the seed key. As shown, some of the seed key is a random seed which unravels the bottom image, while other parts highlight basic information to allow for knowing what to unseed. | 

## Test Calculations 

To see the size of your image with the bitwise_8X1 and 4X1 methods, use [this link](https://raw.githack.com/jeremybeeman/Steganography-Join-2-Images/main/resized_img_size_calc.html).

## Options 

### Data Accessibility Options

| Option      | Meaning                                                                                         |
|:-----------:|:-----------------------------------------------------------------------------------------------:|
| simple      | Combines the top and bottom images together directly, without mixing the data. Doesn't need a seed to access the data                 |
| seeded      | Combines the top and bottom images together via mixing the image using a permutation guided by a seed. Without the seed, the bottom image is inaccessible.                   |

### Data to Encode Options

| Option      | Meaning                                                                                         |
|:-----------:|:-----------------------------------------------------------------------------------------------:|
| pixelwise      | Encodes images into the top image based off of direct pixels. This type of encoding method generally results in a loss of the colors able to be represented in the bottom image                 |
| bitwise      | Encodes images into the top image based off of the pixels 8-bit information. Works with 8-bit images. Perserves the original colors of the original bottom image, but has to shrink the image to a smaller size to fit within the top image                  |

### Size Indication Options 

| Option      | Meaning                                                                                         |
|:-----------:|:-----------------------------------------------------------------------------------------------:|
| 1X1      | The bottom image will be the same size as the top image                       |
| 8X1      | The bottom image is significantly smaller than the top image                  |
| 4X1      | The bottom image is smaller than the top image, but not as extreme. Affects multiple bottom bit layers of the top image to encode the bottom image  |


## Image Citations 

Thanks to Pixabay's free to use license for some of the images shown. For the images from pixabay, see the links below: 
- [Lake Image](https://pixabay.com/images/id-2297204/)
- [Rose Image](https://pixabay.com/images/id-1642970/)
- [Dog Image](https://pixabay.com/images/id-1123016/)
