import os
import cv2
import numpy as np 
import re
import sys 

def drawBoundingBox(image, roi) :
	(x0,y0) = (roi[0], roi[1])
	(x1,y1) = (roi[0] + roi[2], roi[1] + roi[3])
	cv2.rectangle(image, (x0,y0), (x1,y1), (0,255,0), 1)

def scaleIm(image, sf) :
	return cv2.resize(image, (0,0), fx = sf, fy = sf, interpolation = cv2.INTER_NEAREST)

def conformROI(roi) :  # Some ROIs have negative width and height meaning they have been drawn in a negative direction this function sorts that out
	(x,y,w,h) = roi
	if w < 0 or h < 0 :
		return (x + w, y + h, -w, -h)
	else :
		return roi

def getROIs(file) :
	rois_s = re.findall('\([^)]*\)', file.readline())
	rois_i = [ [int(num) for num in roi_s.strip("()").split(",")] for roi_s in rois_s]  # Convert elements : "(123, 231, 123, 234)" -> [123, 231, 123, 234]
	rois_i = [ conformROI(r) for r in rois_i ]
	return rois_i

def cropImage(im, r) :
	(h,w,c) = im.shape
	(y_lo, y_hi) = (r[1], r[1] + r[3])
	(x_lo, x_hi) = (r[0], r[0] + r[2])
	if y_lo <  0 : y_lo = 0 
	if y_hi >= h : y_hi = h - 1 
	if x_lo <  0 : x_lo = 0
	if x_hi >= w : x_hi = w - 1
	return im[y_lo:y_hi, x_lo:x_hi]

def drawCrosshair(image) :
	(h,w,c) = image.shape
	cv2.line(image, (int(w/2), 0), (int(w/2),h), (0,0,0), 3)
	cv2.line(image, (0, int(h/2)), (w,int(h/2)), (0,0,0), 3)
	cv2.line(image, (int(w/2), 0), (int(w/2),h), (0,255,0), 1)
	cv2.line(image, (0, int(h/2)), (w,int(h/2)), (0,255,0), 1)

def drawText(image, text) : 
	cv2.putText(image, text, (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 4)
	cv2.putText(image, text, (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 1)

def drawTextAt(image, text, pos) : 
	cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 4)
	cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 1)

def validateArgvMsg(msg, length) :
	if len(sys.argv) < length :
		print("usage : \n")
		print(str(sys.argv[0]) + " " + msg + "\n")
		sys.exit(0)


def growROI (r, pix) :
	pix = int(pix)
	(x,y,w,h) = r
	x -= int(pix/2)
	y -= int(pix/2)
	w += pix
	h += pix
	return (x,y,w,h)

def dilateROI (r, d) :
	(x,y,w,h) = r
	nw = int(w*d)
	nh = int(h*d)
	x -= int((nw - w)/2)
	y -= int((nh - h)/2)
	(w,h) = (nw,nh)
	return (x,y,w,h)