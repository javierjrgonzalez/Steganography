#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 16:47:14 2022

@author: javiergonzalez
"""

#import libraries
import numpy as np
from PIL import Image

'''
Converting source image into a NumPy array of pixels
Storing the size of the image, RGB image mode equal to 3, calculating total pixels of image.
Summary to encode: Load an image, looks at each pixels in hexademical value, converts secret 
text into bits and stores them in LSB of pixel bits, a delimiter is added to the end of the edited 
pixel values
'''
def Encode(src, message, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
   

    img.mode == 'RGB'
    n = 3

    total_pixels = array.size//n #Gets the total pixels    

    # Adding a delimiter at the end of the secret message
    message += "$t0p!"
    #Converting to binary
    b_message = ''.join([format(ord(i), "08b") for i in message])
    #size of the data to hide
    req_pixels = len(b_message)
    
    
#Checking if the total pixels available is sufficient for the secret message
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

# Modifying the LSB by iterating the pixels one by one and modyfing their lsb to the bits
#of the secret message with the delimiter also hidden
    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 2):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:8] + b_message[index], 2)
                    index += 1


# Updating the pixels array. Creating and saving it as a destination output image.

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")
        
        #Prints the rbg pixel matrices of the image
        #print(array)



#Saving the pixels of the source image as an array and calculating the total pixels
#While retrieving all the 0s and 1s extracted until delimiter is found. Extracted bits are 
#converted into string(secret message)

def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))
    
    #prints the image's rbg pixel matrices
    print(array)
    
    if img.mode == 'RGB':
        n = 3

    total_pixels = array.size//n

#Extracting the LSB from each of the pixels starting from the top-left of the image; storing 
#in it in groups of 8. Converting the groups into ASCII characters to find the hidden msg until 
#delimiter is read. If the delimiter is not found, there is no hidden message in image.

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 2):
            hidden_bits += (bin(array[p][q])[2:][-1])

#splitting by 8-bits
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
#convert from bits to characters
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t0p!":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t0p!" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")
        
    #This will print the long list of 0s and 1s bits after image message is processed
    #print(hidden_bits)
    

#main function
#Ask user which function to perform
def Stego():
    print("--Welcome to Steganography--")
    print("1: Encode")
    print("2: Decode")

    func = input()

    if func == '1':
        print("Enter the source image path")
        src = input()
        print("Enter the message to hide")
        message = input()
        print("Enter destination image path")
        dest = input()
        print("Encoding...")
        Encode(src, message, dest)

    elif func == '2':
        print("Enter the source image path")
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")

Stego()

