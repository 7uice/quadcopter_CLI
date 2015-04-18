#!/usr/bin/env python2

import sys, fileinput, re

#struct GeodeticPosition {
#  long latitude;
#  long longitude;
#  long altitude;
#};

DEBUG = True

# Go through input file and grab all specified coordinates => lat_long_arr
lat_long_arr = []
with open(sys.argv[1], 'r') as infile:
	for line in infile:
		lat_long = line.split(" ")
		if len(lat_long) < 2:
			continue
		lat_long[0] = float(lat_long[0].strip())
		lat_long[1] = float(lat_long[1].strip())
		lat_long.append(0) # append 0 for altitude (we are not currently supporting altitude specification through coordinates)
		lat_long_arr.append(lat_long)
	if DEBUG: print "debug: " + str(lat_long_arr)

# Go through lat_long_arr and generate raw code to insert into AeroQuad.h
# First, create a new GeodeticPosition variable for each waypoint in the input file
raw_code = '\n'
for index,coord in enumerate(lat_long_arr):
	raw_code += "\tGeodeticPosition wp" + str(index) + " = new GeodeticPosition(" + str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + ");\n" 
raw_code += '\n'

# Now, add all the GeodeticPosition variables to the waypoint array
raw_code += "\tGeodeticPosition waypoint[" + str(len(lat_long_arr)) + "] = {\n"
tmp = '\t\t'
for i in range(len(lat_long_arr)):
	tmp += "wp" + str(i)
	if i < len(lat_long_arr) -1:
		tmp += ", "

tmp += "\n\t};\n"
raw_code += tmp
if DEBUG: print raw_code

# Now, find and replace the relevant code inside of AeroQuad.h using regex search/replace
#for line in fileinput.input("test.txt", inplace=True):
#	if "GeodeticPosition waypoint[" in line:
#		line = raw_code
#		print line
#	else:
#		print line.strip()
	#line = re.sub('GPS_INVALID_POSITION','hello!',line.rstrip())
	#print "Line: " + line

#with open("test.txt", 'rw') as f:
#	print "--begin file--"
#	f_str = f.read()
#	print f_str
#	print "--end file--"
#
#	f_str.index("
