import os
import sys
import glob
import time
import random
from PIL import Image
#import win32api, win32con, win32gui
from subprocess import call
from pathlib import Path

# Python 3 Script

# Variables for directories (one for each monitor/resolution)
dir1 = []
dir2 = []

if os.name == "posix":
    folder = "/mnt/c"
else:
    folder = "C:"

root_path = Path(folder + "/Users/peng.f/Pictures/desktop-background")
win_path = Path("C:/Users/peng.f/Pictures/desktop-background")
pwd = Path(os.getcwd())

# Let's move into directory which contains the images
# > Make sure to change below to directory
# > where you have saved your background images.
# os.chdir(root_path)

# Get images from both directories
# Each directory is equivalent to monitor's resolution
# > Change directories to match your resolution / dir name

def getImages():
	global dir1
	global dir2
	#os.chdir("left")
	#dir1 = glob.glob('./*.jpg')
	dir1 = list((root_path / 'left').glob('./*.jpg'))

	# os.chdir("../right")
	# dir2 = glob.glob('./*.jpg')
	dir2 = list((root_path / 'right').glob('./*.jpg'))
	# Return to original directory
	#os.chdir("..")
	print(dir1)
	print(dir2)



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

# Function to actually set the wallpaper as tiled image
# > We will set background as a single image (which is 2 images merged)
def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "1")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)

def make_1920x1080(im, min_size=256, fill_color=(0,0,0,0)):
	new_im = Image.new('RGBA', (1920,1080), fill_color)
	width, height = im.size
	aspect_ratio = width / height
	# size = max(min_size, width, height)
	if aspect_ratio > (16/9):
		# Wider
		# Use width
		scale_ratio = width / 1920		
		
	else:
		# Narrorer
		# Use height
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
print("\n> Changing images: \n\t*" + str(img1) + "\n\t*" + str(img2))

# Merge both images into a single image
mergeIMG(img1, img2)

# Finally we'll set the wallpaper as tiled image

# setWallpaper(root_path + '\\final.jpg')
call(['python.exe', '-c', 'import os; print(os.getcwd())'])
call(["python.exe", "winChangeBackground.py", win_path / 'final.jpg'])