import cv2
import numpy as np 
import os # Operating System 
import re # Regular expressions
import sys

import isak

def num_files_in_dir(dir) :
    num_files = 0
    for file in os.listdir(dir) :
        num_files += 1 
    return num_files

# This function does dynamic print "overwriting" useful for 
# indicating progress 
class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r" + data.__str__())
        sys.stdout.flush()

if len(sys.argv) < 3 :
	print("Loops through images in provided directory and lets user select two ROIs per image\n")
	print("usage: ")
	print(str(sys.argv[0]) + " <image directory> <name of output roi file> ")
	sys.exit(0)

im_dir = os.fsencode(str(sys.argv[1]))
roi_file = open(str(sys.argv[2]), "w")

total_num_images = len(os.listdir(im_dir))

ctr = 0
for file in os.listdir( im_dir ) :
	Printer(str(ctr) + " / " + str(total_num_images))
	print("\n")
	image_name = os.fsdecode(file)
	image_dir_name = os.fsdecode(im_dir)
	im = cv2.imread(image_dir_name + "\\" + image_name)
	# Mark two regions of interest in the current image and save coordinates to file
	roi_file.write(image_name + " : ")
	for i in range(2) :
		ROI = cv2.selectROI(im) 	# User selects ROI
		roi_file.write(str(ROI)) 	# Write coordinates to file
	roi_file.write("\n")
	ctr += 1

roi_file.close()

# For Debug purposes to check that bounding boxes are stored properly in file
# Read bounding boxes from file "one line at a time"
#roi_file = open("rois.txt", "r")
#rois_s = re.findall('\([^)]*\)', roi_file.readline())
#rois_i = [ [int(num) for num in roi_s.strip("()").split(",")] for roi_s in rois_s]  # Convert elements : "(123, 231, 123)" -> [123, 231, 123]


# Draw bounding boxes 
#for roi_i in rois_i :
#	drawBoundingBox(im, roi_i)

#cv2.imshow("image", im)

#key = cv2.waitKey(0)
#print(key)
