# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:15:19 2021

@author: mingke.li
"""

from PIL import Image
from PIL import ImageOps
import sys
import glob

# Trim all png images with white background in a folder
# Usage "python PNGWhiteTrim.py ../someFolder"

# try:
#     folderName = sys.argv[1]
# except :
#     print ("Usage: python PNGWhiteTrim.py ../someFolder")
#     sys.exit(1)

folderName = r"G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Oct\NRCan_python_Oct\Result\vege_img_25"
filePaths = glob.glob(folderName + "/*.png") #search for all png images in the folder

for filePath in filePaths:
    image=Image.open(filePath)
    image.load()
    imageSize = image.size
    
    # remove alpha channel
    invert_im = image.convert("RGB") 
    
    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()
    
    cropped=image.crop(imageBox)
    print (filePath, "Size:", imageSize, "New Size:", imageBox)
    cropped.save(filePath)