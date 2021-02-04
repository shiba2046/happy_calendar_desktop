#!/usr/bin/env python3
'''
bgChanger3.py
Change the Windows background for dual screen
Pictures folder: %USERPROFILE%/Pictures/desktop-background

Change background's code is credited to: 
[Python Background Changer in Windows 10 (Dual Monitor)]
(https://codeonby.com/2019/12/17/python-background-changer-dual-monitor/)

Modified by: Chiba2046
Last modifed: 04 Jan 2021
'''
import os
import sys
import glob
import time
import random
from PIL import Image
#import win32api, win32con, win32gui
from subprocess import run
import wsl

# Python 3 Script

# Variables for directories (one for each monitor/resolution)
dir1 = []
dir2 = []


root_path = wsl.USERPROFILE / 'Pictures/desktop-background'

def getImages():
	global dir1
	global dir2
	dir1 = list((root_path / 'left').glob('./*.jpg'))
	dir2 = list((root_path / 'right').glob('./*.jpg'))

# Merge 2 images together
def mergeIMG(img1, img2):
	img1 = root_path / 'left' / img1
	img2 = root_path / 'right' / img2
	images = [make_1920x1080(Image.open(x)) for x in [img1, img2]]
	
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
	  new_im.paste(im, (x_offset,0))
	  x_offset += im.size[0]
 
	new_im.save( root_path / 'final.jpg', quality=100, subsampling=0)

def make_1920x1080(im, min_size=256, fill_color=(0,0,0,0)):
	new_im = Image.new('RGBA', (1920,1080), fill_color)
	width, height = im.size
	aspect_ratio = width / height
	# size = max(min_size, width, height)
	if aspect_ratio > (16/9): # Wider than 16:9
		# Use width to work out scale ratio
		scale_ratio = width / 1920		
		
	else:		# Narrorer than 16:9
		# Use height to work out scale ratio
		scale_ratio = height / 1080

	new_width = int(width / scale_ratio)
	new_height = int(height / scale_ratio)
	
	print(f'{new_width}x{new_height}, scaled by {scale_ratio} : {aspect_ratio} ')
	
	im = im.resize((new_width, new_height))

	new_im.paste(im, (int((1920 - new_width)/2), int((1080 - new_height)/2)))
	return new_im
	

# ================================================================ #

# Let's get all images from both directories
getImages()


# Main program loop to switch images
# Randomly select a image from each directory
img1 = dir1[(random.randrange(0,len(dir1)))]
img2 = dir2[(random.randrange(0,len(dir2)))]

# Print message showing each image's name
print(f"\n> Changing images: \n\t*{str(img1)}\n\t*{str(img2)}")

# Merge both images into a single image
mergeIMG(img1, img2)

# Finally we'll set the wallpaper as tiled image

# Run the change background script in Windows enviroment
run(["python.exe", "winChangeBackground.py", root_path / 'final.jpg'])