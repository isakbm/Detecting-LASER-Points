import numpy as np
import cv2
import os

import sys

def unitAdjust(x) :
	x -= x.min()
	x /= x.max()
	return x

def num_files_in_dir(dir) :
    num_files = 0
    for file in os.listdir(dir) :
        num_files += 1 
    return num_files

def medianBlur_f(image, ksize) :
	image *= 255.0
	image = image.astype(np.uint8)
	image = cv2.medianBlur(image, ksize).astype(float)/255.0
	return image

def stretch(c) :
	c += 0.5
	c *= c
	return np.clip(c, 0.0, 1.0)

input_dir_str = str(sys.argv[1])

input_dir = os.fsencode(input_dir_str)

total = num_files_in_dir(input_dir)

for img_file in os.listdir(input_dir) :
	file_name = os.fsdecode(img_file)
	img = cv2.imread(input_dir_str + "\\" + file_name)

	# Creates copies of color channels and adjust range to [0,1]
	img_f = img.astype(float)/255.0
	(B,G,R) = cv2.split(img_f)  
	(B,G,R) = map(unitAdjust, (B,G,R))

	grayscale = (B + G + R + 0.00001)  # Small constant added to avoid div by zero



	

	# red-filter
	r = np.copy(R)
	# r *= r
	r_filt = r/grayscale
	r_filt = (r*r)/((G +r + 0.000001)*(B + r + 0.000001))
	# r_filt *= grayscale
	r_filt = unitAdjust(r_filt)
	# r_filt *= r_filt
	# r_filt *= r_filt
	# r_filt = stretch(r_filt)

	# blue-filter
	b = np.copy(B)
	# b *= b
	b_filt = b/grayscale
	b_filt = medianBlur_f(b_filt,15)
	# b_filt = unitAdjust(b_filt)
	# b_filt *= b_filt

	# green-filter
	g = np.copy(G)
	# g *= g
	g_filt = g/grayscale
	g_filt = medianBlur_f(g_filt,15)
	# g_filt = unitAdjust(g_filt)
	# g_filt *= g_filt

	# out
	out = r_filt  #- b_filt - g_filt
	out = unitAdjust(out)
	# out *= out
	# out = stretch(out)
	# out *= out
	temp = out*255.0
	cv2.imshow("test", temp.astype(np.uint8))
	cv2.waitKey()

	# out = medianBlur_f(out, 5)
	# out = unitAdjust(out)
	# out *= out
	# out = medianBlur_f(out, 5)
	# out = unitAdjust(out)
	# out *= out
	out = 255.0*out


	# out = cv2.medianBlur(out, 5)
	
	#ret, out = cv2.threshold(out,100,255,cv2.THRESH_BINARY)
	# img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

	cv2.imshow("test", img.astype(np.uint8))
	cv2.waitKey()