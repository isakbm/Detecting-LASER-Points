import cv2
import numpy as np
import os
from shutil import copyfile


import sys

# This function does dynamic print "overwriting" useful for 
# indicating progress 
class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r" + data.__str__())
        sys.stdout.flush()

if __name__ == '__main__' :

	if len(sys.argv) < 4 :
		print("usage : \n")
		print(str(sys.argv[0]) + " <input directory> <output directory> <file_name_start_counter>\n")
		sys.exit(0)

	from_dir = str(sys.argv[1])
	to_dir = str(sys.argv[2])
	start_count = int( str(sys.argv[3]) )

	# os.mkdir(to_dir)

	directory = os.fsencode(from_dir)
	file_num = start_count
    
    # Convert images to jpg and place into image_jpg directory
	num_files = 0
	for file in os.listdir(directory) :
	    num_files += 1 

	for file in os.listdir(directory):
	    filename = os.fsdecode(file)
	    
	    copyfile(from_dir + "\\" + filename, to_dir + "\\" + str(file_num))

	    new_fname = to_dir + "\\" + "image_" + str(file_num).zfill(4) + ".jpg"

	    Printer(str(file_num + 1) + " / " + str(num_files))

	    im = cv2.imread(to_dir + "\\" + str(file_num) )
	    cv2.imwrite(new_fname, im)
	    
	    os.remove(to_dir + "\\" + str(file_num))

	    file_num += 1

	print("\n\n conversion completed!")

