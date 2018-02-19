import os # Operating System 
import sys

import isak

isak.validateArgvMsg("<directory> <dat file>", 3)	

directory = str(sys.argv[1])
samp_dir = os.fsencode(directory)

dat_file = open(str(sys.argv[2]), "w")

for im_file in os.listdir(samp_dir) :
	im_name = directory + "\\" + os.fsdecode(im_file)
	dat_file.write(im_name + "\n")

dat_file.close()