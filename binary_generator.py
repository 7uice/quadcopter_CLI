#!/usr/bin/env python2

import sys, fileinput, re, os

#struct GeodeticPosition {
#  long latitude;
#  long longitude;
#  long altitude;
#};

DEBUG = False

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
raw_code = "\tGeodeticPosition waypoint[" + str(len(lat_long_arr)) + "] = {"
for index,coord in enumerate(lat_long_arr):
	raw_code += "new GeodeticPosition(" + str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + ")" 
	if index != len(lat_long_arr) -1:
		raw_code += ", "	
raw_code += "};\n\n"

if DEBUG: print raw_code

# Reset AeroQuad.h bc too lazy to do this any other way
if os.path.exists("AeroQuad.h.orig"):
	os.system("cp AeroQuad.h.orig AeroQuad.h")

# Now, find and replace the relevant code inside of AeroQuad.h using regex search/replace
for line in fileinput.input("AeroQuad.h", inplace=True):
	if "GeodeticPosition waypoint[" in line:
		line = raw_code
		print line
	else:
		print line.strip()

# Now attempt to make the code
os.system("make -C Libmaple/libmaple library")
os.system("make -C BuildAQ32")
print "Binary should be located at /BuildAQ32/objSTM32/AeroQuad32/AeroQuadMain.bin"
