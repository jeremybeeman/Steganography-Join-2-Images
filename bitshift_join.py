import cv2
import numpy as np 
import math 
import random 

#NOTE: The loopMax needs to be modified to reflect ALL of the bits/pixels. Missing 1 bit/pixel in all but the seeded_bitwise_8X1
class bitshift_join():

    def resize_images(front_image_path, back_image_path, interpolation=cv2.INTER_AREA):
        # Makes the images the same size, then joins them, each pixel to each pixel. 
        # Goes off of the smallest image's size (prioritizes front image's size over bottom, so one has smaller width and other has bigger height, front image's size is chosen)
        imgfront = cv2.imread(front_image_path, cv2.IMREAD_COLOR)
        imgbehind = cv2.imread(back_image_path, cv2.IMREAD_COLOR)
        shapeFront = imgfront.shape
        shapeBehind = imgbehind.shape 
        if shapeFront[0] < shapeBehind[0] or shapeFront[1] < shapeBehind[1]: 
            imgbehind = cv2.resize(imgbehind, [shapeFront[1], shapeFront[0]], interpolation) 
        elif shapeFront[0] >= shapeBehind[0] and shapeFront[1] >= shapeBehind[1]: 
            imgfront = cv2.resize(imgfront, [shapeBehind[1], shapeBehind[0]], interpolation)
        return [imgfront, imgbehind]
        #doesn't resize when both are equal 

    def simple_pixelwise_1X1_encode(front_image_path, back_image_path, bits_used_by_front, interpolation=cv2.INTER_AREA):
        # joins the two images together using a 1X1 ratio. 
        [imgfront, imgbehind] = bitshift_join.resize_images(front_image_path, back_image_path, interpolation)

        #joins the two images
        imgjoin = np.uint8(np.uint8(imgfront >> (8-bits_used_by_front)) << (8-bits_used_by_front)) # removes bottom bits for joining
        imgjoin = imgjoin + np.uint8(imgbehind >> bits_used_by_front) # places the bottom image in 
        return np.array(imgjoin, dtype="uint8")

    def simple_pixelwise_1X1_decode(encoded_image_path, bits_used_by_front):
        # decodes an image that has been joined via simple 1X1 bitshifting 
        # returns BOTH images, the top image in the 0th index and the bottom image in the 1st index
        joinedImg = cv2.imread(encoded_image_path, cv2.IMREAD_COLOR)
        imgTop = np.uint8((joinedImg >> (8-bits_used_by_front)<<(8-bits_used_by_front)))
        imgBottom = np.uint8(joinedImg << bits_used_by_front)

        return [np.array(imgTop, dtype="uint8"), np.array(imgBottom, dtype="uint8")]

    def seedKeyGen(imgShape, numBitPlanes, unusedBits, bottomImgShape): 
        #generates a string of numbers and letters that equivocate to the seed. 
        #numBitPlanes refers to the number of bottom bits to be used for the code
        #generates the key based off of a number and a letter
        #numberLetternumberLetternumberLetter 
        #all numbers are directly the numbers they specify. The letter's placement is used (where a=1, b=2, and so on)
        
        if numBitPlanes > 8: 
            raise Exception("Cannot generate a key with more than 8 bit planes (you want to create an image outside of the 8-bit limitation)")
        seedKey = ""
        lowerABCs = list(range(ord('a'), ord('z')+1))
        topSeed = random.randint(0, numBitPlanes-1)
        if topSeed == 0:
            seedKey = seedKey + "0" + chr(random.choice(lowerABCs))
        else: #simple for now. If greater than 1, then just use a
            seedKey = seedKey + str(topSeed) + "a"

        #for the middle piece
        for i in range(0, 2):
            SeedNum = random.randint(1, imgShape[i]-1)
            SeedLetter = random.randint(lowerABCs[0], lowerABCs[0]+(imgShape[i]-1)//SeedNum-1)
            if SeedLetter > lowerABCs[len(lowerABCs)-1]: 
                SeedLetter = random.randint(lowerABCs[0], lowerABCs[len(lowerABCs)-1])
            seedKey += str(SeedNum) + chr(SeedLetter) 
        
        #for any bits that will be overloaded, the last bit tells how many unused bits to start with. Is 0 for all pixelwise operations
        seedKey += str(unusedBits) + "a" #for the (index 0)
        seedKey += str(bottomImgShape[0]) + "a" 
        seedKey += str(bottomImgShape[1]) + "a"
        return seedKey

    def seedKeyExtract(seedKey):
        #extracts the seed key created by seedKeyGen
        seedLoc = [0, 0, 0, 0, 0, 0]
        currSeedLoc = 0
        currNum = 0
        #extracts the seed numbers
        for i in range(0, len(seedKey)):
            if ord(seedKey[i]) >= ord('a') and  ord(seedKey[i]) <= ord('z'): #if the letter, multiply letter by number
                seedLoc[currSeedLoc] = currNum * (ord(seedKey[i])-ord('a')+1)
                currSeedLoc += 1
                currNum = 0
            elif ord(seedKey[i]) >= ord('0') and  ord(seedKey[i]) <= ord('9'): #if a number, number to be multiplied by letter
                currNum = currNum * 10 + int(seedKey[i])
            else:
                raise Exception("not valid seed. All seeds consist of numbers and lowercase letters. Nothing else.")
        return seedLoc 
    
    def seeded_pixelwise_1X1_encode(front_image_path, back_image_path, bits_used_by_front, seedKey = "", interpolation=cv2.INTER_AREA):
        # creates the front/back images with a seed key. If no seed key is specified, then a seed key is generated
        # joins the two images together using a 1X1 ratio. 
        # lossy means it is joined pixel by pixel, instead of bit by bit
        [imgfront, imgbehind] = bitshift_join.resize_images(front_image_path, back_image_path, interpolation)
        if not seedKey:
            seedKey = bitshift_join.seedKeyGen(imgfront.shape, 1, 0, imgbehind.shape)
        seedKeyDecode = bitshift_join.seedKeyExtract(seedKey)
        loopMax = imgfront.shape[0]*imgfront.shape[1]
        newPixelLoc = np.random.RandomState(seed=seedKeyDecode[1]*seedKeyDecode[2]).permutation(loopMax)
        imgfront= np.uint8(np.uint8(imgfront >> (8-bits_used_by_front)) << (8-bits_used_by_front)) # removes bottom bits for joining
        imgbehind = np.uint8(imgbehind >> bits_used_by_front) # sets up the pixels for joining
        for i in range(0, loopMax):
            frontLoc = [i % imgfront.shape[0], (i//imgfront.shape[0])]
            backLoc = [newPixelLoc[i] % imgfront.shape[0], (newPixelLoc[i]//imgfront.shape[0])]
            imgfront[frontLoc[0]][frontLoc[1]] += imgbehind[backLoc[0]][backLoc[1]]

        return [np.array(imgfront, dtype="uint8"), seedKey]
    
    def seeded_pixelwise_1X1_decode(encoded_image_path, bits_used_by_front, seedKey):
        #decodes a seeded image based off of the seed used
        seedKeyDecode = bitshift_join.seedKeyExtract(seedKey)
        # decodes an image that has been joined via simple 1X1 bitshifting 
        # returns BOTH images, the top image in the 0th index and the bottom image in the 1st index
        joinedImg = cv2.imread(encoded_image_path, cv2.IMREAD_COLOR)
        imgTop = np.uint8((joinedImg >> (8-bits_used_by_front))<<(8-bits_used_by_front))
        imgBottom = np.uint8(joinedImg << bits_used_by_front)
        imgReformat = np.zeros(imgBottom.shape, np.uint8)
        loopMax = joinedImg.shape[0]*joinedImg.shape[1]
        pixelLoc = np.random.RandomState(seed=seedKeyDecode[1]*seedKeyDecode[2]).permutation(loopMax)
        for i in range(0, loopMax):
            frontLoc = [i % joinedImg.shape[0], (i//joinedImg.shape[0])]
            backLoc = [pixelLoc[i] % joinedImg.shape[0], (pixelLoc[i]//joinedImg.shape[0])]
            imgReformat[backLoc[0]][backLoc[1]] += imgBottom[frontLoc[0]][frontLoc[1]]  

        return [np.array(imgTop, dtype="uint8"), np.array(imgReformat, dtype="uint8")]

    def simple_bitwise_8X1_encode(front_image_path, back_image_path, interpolation=cv2.INTER_AREA):
        #current model: 12/21/21 shrinks the image to a scaled proportion that will fit within the 8-bit constraint of the top image. 
        #this is done after resize
        # joins the two images together using a 1X1 ratio. 
        #if it's not a perfect fit, then some of the pixels generated will not mean anything
        #those bits will be the first few that are required. 
        #the seed code will include a blurb about the bits that are missing at the very end
        #the unused bits will be placed at the start
        #bits are placed in little endian 
        [imgfront, imgbehind] = bitshift_join.resize_images(front_image_path, back_image_path, interpolation)
        bits_possible = imgfront.shape[0] * imgfront.shape[1] 
        pixels_possible = bits_possible//8 
        scale_bottom = imgbehind.shape[0]/imgbehind.shape[1] #gets a ratio of 0th to 1st to determine

        height_bottom = int(math.sqrt(pixels_possible//scale_bottom))
        width_bottom = int(height_bottom * scale_bottom)
        imgbehind = cv2.resize(imgbehind, [width_bottom, height_bottom], interpolation)
        bits_used_by_front = 7
        unusedBits = bits_possible - width_bottom*height_bottom*8
        ##joins the two images
        imgjoin = np.uint8(np.uint8(imgfront >> (8-bits_used_by_front)) << (8-bits_used_by_front)) # removes bottom bits for joining
        loopMax = imgjoin.shape[0]*imgjoin.shape[1]
        currBit = 0 
        currPixel = 0 
        #loops through the whole top image and joins
        for i in range(0, loopMax):
            if i >= unusedBits:
                frontLoc = [i % imgjoin.shape[0], (i//imgjoin.shape[0])]
                backLoc = [currPixel % imgbehind.shape[0], (currPixel//imgbehind.shape[0])]
                #places the current bit of the bottom image into the top image
                imgjoin[frontLoc[0]][frontLoc[1]] += np.uint8((imgbehind[backLoc[0]][backLoc[1]] & (1<<currBit)) >> currBit)
                currBit += 1
                if currBit > 7: 
                    currBit = 0 
                    currPixel += 1
        return [np.array(imgjoin, dtype="uint8"), unusedBits, width_bottom, height_bottom]

    def simple_bitwise_8X1_decode(encoded_image_path, unusedBits, width_bottom, height_bottom):
        bits_used_by_front = 7
        joinedImg = cv2.imread(encoded_image_path, cv2.IMREAD_COLOR)
        imgTop = np.uint8((joinedImg >> (8-bits_used_by_front)<<(8-bits_used_by_front)))
        height_bottom = ((imgTop.shape[0] * imgTop.shape[1]) - unusedBits)//(width_bottom*8) #pulls the height out from the width
        imgBottom = np.zeros([height_bottom,  width_bottom, 3], np.uint8)
        loopMax = joinedImg.shape[0]*joinedImg.shape[1]
        currBit = 0 
        currPixel = 0 
        for i in range(0, loopMax):
            if i >= unusedBits: #once the unused bits have been skipped, join
                frontLoc = [i % joinedImg.shape[0], (i//joinedImg.shape[0])]
                backLoc = [currPixel % imgBottom.shape[0], (currPixel//imgBottom.shape[0])]
                imgBottom[backLoc[0]][backLoc[1]] |= ((joinedImg[frontLoc[0]][frontLoc[1]] & 1) << currBit) #isolates the current bit and ors it with the current pixel
                currBit += 1
                if currBit > 7: 
                    currBit = 0 
                    currPixel += 1
        return [np.array(imgTop, dtype="uint8"), np.array(imgBottom, dtype="uint8")]

    def seeded_bitwise_8X1_encode(front_image_path, back_image_path, seedKey="", interpolation=cv2.INTER_AREA):
        [imgfront, imgbehind] = bitshift_join.resize_images(front_image_path, back_image_path, interpolation)
        #handles the scaling for the image
        bits_possible = imgfront.shape[0] * imgfront.shape[1] 
        pixels_possible = bits_possible//8 
        scale_bottom = imgbehind.shape[0]/imgbehind.shape[1] #gets a ratio of 0th to 1st to determine
        height_bottom = int(math.sqrt(pixels_possible//scale_bottom))
        width_bottom = int(height_bottom * scale_bottom)
        imgbehind = cv2.resize(imgbehind, [width_bottom, height_bottom], interpolation)
        #specifies the unused bits 
        bits_used_by_front = 7
        unusedBits = bits_possible - width_bottom*height_bottom*8
        #generates the seedKey(if needed)
        if not seedKey: 
            seedKey = bitshift_join.seedKeyGen(imgfront.shape, 1, unusedBits, imgbehind.shape) #coded off of the BOTTOM image
        seedKeyDecode = bitshift_join.seedKeyExtract(seedKey)
        #creates the random permutation based on the top image size 
        loopMax = imgfront.shape[0]*imgfront.shape[1]
        pixelLoc = np.random.RandomState(seed=seedKeyDecode[1]*seedKeyDecode[2]).permutation(loopMax)
        ##joins the two images
        imgjoin = np.uint8(np.uint8(imgfront >> (8-bits_used_by_front)) << (8-bits_used_by_front)) # removes bottom bits for joining
        currBit = 0 
        currPixel = 0 
        #loops through the whole top image and joins
        for i in range(0, loopMax):
            if i >= unusedBits:
                frontLoc = [pixelLoc[i] % imgjoin.shape[0], (pixelLoc[i]//imgjoin.shape[0])]
                backLoc = [currPixel % imgbehind.shape[0], (currPixel//imgbehind.shape[0])]
                #places the current bit of the bottom image into the top image
                imgjoin[frontLoc[0]][frontLoc[1]] += np.uint8((imgbehind[backLoc[0]][backLoc[1]] & (1<<currBit)) >> currBit)
                currBit += 1
                if currBit > 7: 
                    currBit = 0 
                    currPixel += 1
        return [np.array(imgjoin, dtype="uint8"), seedKey]

    def seeded_bitwise_8X1_decode(encoded_image_path, seedKey):
        seedKeyDecode = bitshift_join.seedKeyExtract(seedKey)
        #extracting the unused bits, width, and hight of bottom image
        bits_used_by_front = 7
        joinedImg = cv2.imread(encoded_image_path, cv2.IMREAD_COLOR)
        imgTop = np.uint8((joinedImg >> (8-bits_used_by_front)<<(8-bits_used_by_front)))
        unusedBits = seedKeyDecode[3]
        width_bottom = seedKeyDecode[4]
        height_bottom = seedKeyDecode[5]
        #sets up the loop/image to contain bottom image
        imgBottom = np.zeros([width_bottom, height_bottom, 3], np.uint8)
        loopMax = joinedImg.shape[0]*joinedImg.shape[1]
        currBit = 0 
        currPixel = 0 
        pixelLoc = np.random.RandomState(seed=seedKeyDecode[1]*seedKeyDecode[2]).permutation(loopMax)
        for i in range(0, loopMax):
            if i >= unusedBits: #once the unused bits have been skipped, join
                frontLoc = [pixelLoc[i] % joinedImg.shape[0], (pixelLoc[i]//joinedImg.shape[0])]
                backLoc = [currPixel  % imgBottom.shape[0], (currPixel //imgBottom.shape[0])]
                imgBottom[backLoc[0]][backLoc[1]] |= ((joinedImg[frontLoc[0]][frontLoc[1]] & 1) << currBit) #isolates the current bit and ors it with the current pixel
                currBit += 1
                if currBit > 7: 
                    currBit = 0 
                    currPixel += 1
        return [np.array(imgTop, dtype="uint8"), np.array(imgBottom, dtype="uint8")]
