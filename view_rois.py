import os
import cv2
import numpy as np 
import re
import sys 

import isak # my own library of useful functions

isak.validateArgvMsg("<image directory> <roi file name>", 3)

im_dir_name = str(sys.argv[1])
roi_file = open( str(sys.argv[2]) )
im_dir = os.fsencode(im_dir_name)

for file in os.listdir(im_dir) :
	
	file_name = os.fsdecode(file)
	im = cv2.imread(im_dir_name + "\\" + file_name)

	for roi in isak.getROIs(roi_file) :
		roi = tuple(abs(r) for r in roi)
		cropped = isak.cropImage(im, roi)
		(h, w, c) = cropped.shape
		sf = 1200.0/(max(w,h))
		cropped = cv2.resize(cropped, (0,0), fx=sf, fy=sf, interpolation = cv2.INTER_NEAREST)
		
		# Graphical information
	
		isak.drawText(cropped, str(w) + " x " + str(h))
		isak.drawCrosshair(cropped)

		cv2.imshow("test", cropped)
		cv2.waitKey()

roi_file.close()