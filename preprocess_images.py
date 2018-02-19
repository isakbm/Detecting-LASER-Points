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

input_dir_str = str(sys.argv[1])
output_dir_str = str(sys.argv[2])

input_dir = os.fsencode(input_dir_str)

total = num_files_in_dir(input_dir)

counter = 1 
for img_file in os.listdir(input_dir) :
	file_name = os.fsdecode(img_file)
	img = cv2.imread(input_dir_str + "\\" + file_name)

	# Creates copies of color channels and adjust range to [0,1]
	img_f = img.astype(float)/255.0
	(B,G,R) = cv2.split(img_f)  
	(B,G,R) = map(unitAdjust, (B,G,R))

	grayscale = B + G + R + 0.00001  # Small constant added to avoid div by zero

	# red-filter
	r = np.copy(R)
	r *= r
	r_thr = (np.greater(r,0.2)).astype(float)  
	r_filt = (r*r_thr)/grayscale
	r_filt = unitAdjust(r_filt)
	r_filt *= r_filt

	# blue-filter
	b = np.copy(B)
	b *= b
	b_filt = b/grayscale
	b_filt = unitAdjust(b_filt)
	b_filt *= b_filt

	# green-filter
	g = np.copy(G)
	g *= g
	g_filt = g/grayscale
	g_filt = unitAdjust(g_filt)
	g_filt *= g_filt

	# out
	out = r_filt - b_filt - g_filt + 2.0
	out = unitAdjust(out)
	out *= out
	# out *= out
	# out *= out
	out = 255.0*out
	(w,h) = out.shape

	# cv2.imshow("test", out/255.0)
	# cv2.waitKey()
	cv2.imwrite(output_dir_str + "\\" + file_name, out)
	print(counter, " of ", total)
	counter += 1