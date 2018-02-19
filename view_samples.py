import os
import cv2
import numpy as np 
import sys

import isak

isak.validateArgvMsg("<samples directory>", 2)

samples_dir_name = str(sys.argv[1])
samples_dir = os.fsencode(samples_dir_name)


files = os.listdir(samples_dir)
num_files = len(files)

ctr = 0 
for file in files :
	file_name = os.fsdecode(file)
	im = cv2.imread(samples_dir_name + "\\" + file_name)
	
	sf = 16.0
	im = cv2.resize(im, (0,0), fx=sf, fy=sf, interpolation = cv2.INTER_NEAREST)

	isak.drawText(im, str(ctr) + "/" + str(num_files) ) 
	cv2.imshow("test", im)

	key = cv2.waitKey()
	if (key == ord('x')) : # then delete that sample
		os.remove(samples_dir_name + "\\" + file_name)

	ctr += 1
