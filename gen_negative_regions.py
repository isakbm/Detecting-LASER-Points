# The idea is we keep everything to the left and the right of the ROI, if it's dims are greater than 20 px 
# Because then it can be used as negative (background) training samples

import cv2
import numpy as np 
import os # Operating System 
import re # Regular expressions
import sys

import isak

# Takes two ROIs (two laser points) and computes their bounding box
def rois_to_xy_bounds(r) : 
	
	x00 = 		r[0][0]
	x01 = x00 + r[0][2]
	y00 = 		r[0][1]
	y01 = y00 + r[0][3]
	
	x10 = 		r[1][0]
	x11 = x10 + r[1][2]
	y10 = 		r[1][1]
	y11 = y10 + r[1][3]

	x_min = min(x00, x10)
	x_max = max(x01, x11)
	y_min = min(y00, y10)
	y_max = max(y01, y11)

	return (x_min, y_min, x_max - x_min, y_max - y_min)

# Image directory
im_dir = str(sys.argv[1])
neg_dir = str(sys.argv[2])

directory = os.fsencode(im_dir)

# Open ROI file
roi_file = open("rois.txt", "r")
neg_dat = open("negatives.dat", "w")

# Create new cropped images from ROIs
counter = 0
for file in os.listdir(directory) :

	# Open image
	im_fname = os.fsdecode(file)

	im = cv2.imread(im_dir + "\\" + im_fname)

	ROIs = isak.getROIs(roi_file)

	# Create cropped images from ROIs

	# Compute bounding boxes for regions that don't contain ROIs
	(bx, by, bw, bh) = rois_to_xy_bounds(ROIs)
	h, w, n_channels = im.shape
	bbox_0 = (       0,       0,          bx,           h )
	bbox_1 = ( bx + bw,       0, w - bx - bw,           h )
	bbox_2 = (      bx,       0,          bw,          by )
	bbox_3 = (      bx, by + bh,          bw, h - by - bh )

	# Cropped bboxs ---> negative images
	bboxs = (bbox_0, bbox_1, bbox_2, bbox_3)
	for bbox in bboxs :
		(x, y, w, h) = bbox
		if w > 24 and h > 24 :  # We make sure that negatives are larger than 20 x 20 (the size of positive samples)
			crop = isak.cropImage(im, bbox)
			im_directory = neg_dir + "\\" + str(counter) + ".jpg"
			cv2.imwrite(im_directory, crop)
			neg_dat.write(im_directory + "\n")
			counter += 1
	

roi_file.close()
neg_dat.close()

