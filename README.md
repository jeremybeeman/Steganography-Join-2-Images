# Steganography-Join-2-Images
This repo focuses on joining two images together via different means. This repo contains a library that joins a top image with a bottom image. The different joins have tradeoffs. 
## Table of Contents 
- [Summary](#summary)
- [Required Software](#required-software)
- [Python Used Modules](#python-used-modules)
- [Before Starting](#notes)
- [Test Calculations Website](#test-calculations)
- [Options (Naming Conventions)](#options)
  * [Data Accessibility Options](#data-accessibility-options)
  * [Data to Encode Options](#data-to-encode-options)
  * [Size Indication Options](#size-indication-options)

## Summary 

This repository combines two images together using various methods of encoding. The method for combining these images together has to do with the fact that images tend to be stored as an unsigned integer. It also relies on that human eyes tend to not respond to very low level brightness differences (that is, the difference between brightness 2 and brightness 1). So, a bottom image can be encoded into the top image's bottom bits. There are two methods to this encoding: pixelwise and bitwise. Pixelwise uses the pixels of the bottom image and combines them with the top image's pixels. This causes the bottom image's colors to be muted in comparison to the original. If preserving the color/brightness of the bottom image, then bitwise encoding is key. This places the brightness levels of the bottom image into the pixels of the top image, instead of the pixel values themselves. This preservesthe color/brightness, but not the original size of the image. 

## Uses 

- Making NFTs more hardened to right-clicking (one can't access the second image without a code). 
- Making ARGs that are tougher to crack. 
- Other stuff.........

## Required Software 

| Software                               | Version (or Comparable)  |
|:--------------------------------------:|:------------------------:|
| Python                                 | 3.9.9                    |
| numpy                                  | 1.20.3                   |
| opencv-contrib-python                  | 4.5.4.60                 |    
| Visual Studio                          | 2019 (16.10.3)           | 

## Python Used Modules 

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
