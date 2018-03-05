from PIL import Image
import pysrt
import utility
import os
import csv
import math
import sys

positions = pysrt.open('/home/jarvis/Desktop/software_dev/videos/DJI_0301.SRT') # path of the srt file
path = "/home/jarvis/Desktop/software_dev/images/" # path of the images folder
totalcount = len(positions) # total number of entries in the srt file

flight_parameter = 35 # flight parameter initialized to 35
if(len(sys.argv) == 2):
	flight_parameter = float(sys.argv[1]) # assigned the value of argument if given

x = 0
turn = 0
limit  = 9
visited = {}
images = []
output_csvfile = []

output_file = open('/home/jarvis/Desktop/software_dev/video_answer.csv','w+') # path of the output csv file
writer = csv.writer(output_file)

while( x < totalcount ): # iterating through all the items in the srt file
	y = 0
	output_csvfile.append( int((x+1)/10) ) # this value gives the second(time) under consideration..
	if turn >= 1:
		limit = 10

	'''
	For every second, there should be 1000 miliseconds.Readings are given in the form of 0-100,100-200,...900-000..
	So for every second, ten consecutive readings should be considered.But for first second, reading 0-100 is missing.
	So only 9 consecutive readings will be considered for first second and similarly 4 readings for the 16th second.
	In between,for all the seconds, 10 consecutive readings will be taken.

	variables 'turn','limit','x' and 'y' are used to take care of this.

	limit variable counts the number of readings to be taken for this particular second.
	A dictionary 'visited' has been used to take care of not checking a image again and again if it has been included in the answer.

	'''

	while( y < limit and x < totalcount ):
		coordinates = positions[x].text.split(',') # this produces a list of text splitted using a ','
		lon1 = float(coordinates[0]) # getting longitude value from srt file
		lat1 = float(coordinates[1]) # getting latitude value from srt file
		print(lon1,lat1)
		x = x + 1
		y = y + 1

		for root, dirs, files in os.walk(path):
			for file_name in files: # iterating through all the images present in the image directory
				extension = file_name[-3:]
				if( extension == "JPG" and file_name not in visited ): # considering only jpg images for now
					filename = path + file_name
					image = Image.open(filename)
					exif_data = utility.get_exif_data(image)
					lon2, lat2 = utility.get_lat_lon(exif_data)
					if lon2 != None and lat2 != None :
						distance = utility.getDistanceFromLatLonInM(lat1,lon1,lat2,lon2) # distance between image and video coords.
						#print(distance)
						if distance <= flight_parameter:
							visited[file_name] = True # marking that this image has been considered for this particular second.
							images.append(file_name)

	output_csvfile.append(images) 
	#print(images)
	print("\n\n")
	writer.writerow(output_csvfile) # append answer to the csv file.
	turn = turn + 1 # this takes care of first second.. a special case that has 9 readings.

	output_csvfile.clear() #clearing the list
	visited.clear() #clearing the dictionary
	images.clear() #clearing the list of images.

output_file.close()
print("Work Done ;p") # mission complete :)
