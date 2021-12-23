# Steganography-Join-2-Images
This repo focuses on joining two images together via different means. This repo contains a library that joins a top image with a bottom image. The different joins have tradeoffs. 
## Table of Contents 
- [Required Software](#required-software)
- [Before Starting](#notes)
- [Options (Naming Conventions)](#options)
  * [Data Accessibility Options](#data-accessibility-options)
  * [Data to Encode Options](#data-to-encode-options)
  * [Size Indication Options](#size-indication-options)

## Required Software 

| Software                               | Version (or Comparable)  |
|:--------------------------------------:|:------------------------:|
| Python                                 | 3.9.7                    |
| Numpy                                  | 1.19.5                   |
| opencv-contrib-python                  | 4.5.3.56                 |                    

## Notes 

- All images MUST be stored as .png instead of .jpeg or .jpg. This is because JPEGs are lossy, and will filter out these encoding methods, as these methods tend to be high frequency. 

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
