import cv2
import numpy as np 
import os # Operating System 
import re # Regular expressions
import sys

import isak

# Image directory

if len(sys.argv) < 4 : 
	print("usage : ")
	print(str(sys.argv[0]) + " <image directory name> <samples output dir name> <roi file name>" )
	sys.exit(0)

img_dir_name = str(sys.argv[1])
crop_dir = str(sys.argv[2])
roi_file_name = str(sys.argv[3])

directory = os.fsencode(img_dir_name)

# Open ROI file
roi_file = open(roi_file_name, "r")

# Create new cropped images from ROIs
im_counter = 1
counter = 0
for file in os.listdir(directory) :

	# Open image
	im_fname = os.fsdecode(file)

	im = cv2.imread(img_dir_name + "\\" + im_fname)

	ROIs = isak.getROIs(roi_file)

	# Create cropped images from ROIs
	for r in ROIs :

		(w,h) = (r[2], r[3])
		L = max(w,h)
		(dw, dh)  = (L - w, L - h)
		new_r = (r[0] - int(dw/2), r[1] - int(dh/2), L, L)
		if new_r[0] < 0 or new_r[1] < 0 :
			print("skipping : negative numbers in cropped roi")
		else :
			print(im_counter, " ", new_r)

			# Crop and scale to 20 x 20 pixels, then increase sample size by creating vertical and horizontal flipped copies
			sf = (20.0/L)
			crop_n_scale = cv2.resize( isak.cropImage(im, new_r) , (0,0), fx=sf, fy=sf, interpolation = cv2.INTER_CUBIC)
			# flip_0 = cv2.flip(crop_n_scale, 0)
			# flip_1 = cv2.flip(crop_n_scale, 1)
			# crop_n_scale = isak.cropImage(im, new_r)

			cv2.imwrite(crop_dir + "\\" + str(counter).zfill(4) + ".jpg", crop_n_scale)
			counter += 1
			# cv2.imwrite(crop_dir + "\\" + str(counter).zfill(4) + ".jpg", flip_0)
			# counter += 1
			# cv2.imwrite(crop_dir + "\\" + str(counter).zfill(4) + ".jpg", flip_1)
			# counter += 1
	im_counter += 1 

roi_file.close()


