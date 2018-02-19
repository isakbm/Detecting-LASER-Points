import numpy as np
import cv2
import os
import sys

import operator as op

import isak

def compCenter(rect) :
	(x1, y1, x2, y2) = rect
	return ( int((x1 + x2)/2), int((y1 + y2)/2) )

def myDetect(img, cascade) :
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=0, minSize=(20, 20),  maxSize=(250, 250))
    if len(rects) == 0:
        return -1
    rects[:,2:] += rects[:,:2]
    centers = list(map(compCenter, rects))
    return centers

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=0, minSize=(20, 20),  maxSize=(250, 250))
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def unitAdjust(x) :
	x -= x.min()
	x /= x.max()
	return x

def preprocess(img) :
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
	# out = r
	out = 255.0*out
	return out.astype(np.uint8)

isak.validateArgvMsg("<cascade xml file> <name of image directory>", 3)

cascade_xml = str(sys.argv[1])
img_dir_name = str(sys.argv[2])

img_dir = os.fsencode(img_dir_name)

for img_file in os.listdir(img_dir) :

	file_name = os.fsdecode(img_file)
	img = cv2.imread(img_dir_name + "\\" + file_name)
	gray = preprocess(img)

	cascade = cv2.CascadeClassifier(cascade_xml)
	centers = myDetect(gray, cascade)
	rects = detect(gray, cascade)

	centers = sorted(centers, key=op.itemgetter(0))

	split = 0
	for i in range(len(centers)-1):
		diff = centers[i+1][0] - centers[i][0]
		if diff > 20 :
			split = i +1
			break

	for c in centers[:split]:
		print(c)
	print(" ========= ")
	for c in centers[split:]:
		print(c)

	(mp1, mp2) = (np.mean(centers[:split], axis=0), np.mean(centers[split:], axis=0))

	for c in (mp1.astype(int), mp2.astype(int)) :
		cv2.circle(img, (c[0],c[1]), 5, (255, 0, 0), 4)
		# print(c)

	
	# draw_rects(img, rects, (0,255,0))
	cv2.imshow("test", img) 

	cv2.waitKey(0)
