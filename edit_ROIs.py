import os
import cv2
import numpy as np 
import re
import sys

import isak

isak.validateArgvMsg("<image directory> <input rois> <output rois>", 4)

samples_dir_name = str(sys.argv[1])
old_rois = str(sys.argv[2])
new_rois = str(sys.argv[3])


beta_rois_file = open(new_rois, "w")
rois_file = open(old_rois, "r")
samples_dir = os.fsencode(samples_dir_name)

files = os.listdir(samples_dir)
num_images = len(files)
img_ctr = 1

for file in files :

	file_name = os.fsdecode(file)
	im = cv2.imread(samples_dir_name + "\\" + file_name)

	beta_rois_file.write(file_name + " : ")
	ctr = 0
	for roi in isak.getROIs(rois_file) :

		g_amount = 20
		g_amount_half = int(g_amount/2)

		(w,h) = roi[2::]
		g_roi = isak.growROI(roi,g_amount)
		roi_im = isak.cropImage(im, g_roi)
		
		scale_f = 1200.0/(max(w,h)+g_amount)
		roi_im = isak.scaleIm(roi_im, scale_f)

		(H ,W, c) = roi_im.shape
		isak.drawBoundingBox(roi_im, isak.growROI((0,0,W,H),-g_amount*scale_f) )
		isak.drawCrosshair(roi_im)
		isak.drawText(roi_im, str(w) + " x " + str(h))
		isak.drawTextAt(roi_im, str(img_ctr) + "/" + str(num_images), (5,100))

		# cv2.imshow("test", roi_im)

		# Get roi and scale back to original pixel coordinates
		n_roi = cv2.selectROI(roi_im, fromCenter=True)
		
		(x, y, w, h) = tuple(int(np.round(a/scale_f)) for a in n_roi)
		
		# Compute better roi
		(X, Y, W, H) = roi
		beta_roi = (X + x - g_amount_half, Y + y - g_amount_half, w, h)
		beta_rois_file.write(str(beta_roi) + " ")

	beta_rois_file.write("\n")
	img_ctr += 1 


rois_file.close()

beta_rois_file.close()