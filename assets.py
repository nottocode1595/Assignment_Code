from PIL import Image
import utility
import os
import math
import csv
import sys

path = "/home/jarvis/Desktop/software_dev/images/"  # path to images folder
output_file = open('/home/jarvis/Desktop/software_dev/assets_answer.csv','w+') # output file where the solution images will be stored
writer = csv.writer(output_file)
flight_parameter = 50  #initialized to 50
if(len(sys.argv) == 2):
	flight_parameter = float(sys.argv[1]) # assign the value of argument

with open('/home/jarvis/Desktop/software_dev/assets.csv','r+') as csvfile:
	reader = csv.reader(csvfile)
	next(reader) 

	for row in reader: #iterating the rows in asset.csv file
		#(lon1 , lat1) = ((float)row[1], (float)row[2]) 

		#coordinates of the POIs from the assets.csv file.
		lon1 = float(row[1]) # reading the longitude value 
		lat1 = float(row[2]) # reading the latitude value
		
		images = []
		for root, dirs, files in os.walk(path): #lists all the files in the directory
			for file_name in files: # iterating in the file list
				extension = file_name[-3:]
				if( extension == "JPG" ): # considering only jpg images for now..for more extensions, cases can be added here.
					filename = path + file_name
					image = Image.open(filename)
					exif_data = utility.get_exif_data(image) #getting the exif data of the image
					lon2, lat2 = utility.get_lat_lon(exif_data) # getting the lon-lat from the exif data
					if lon2 != None and lat2 != None :
						distance = utility.getDistanceFromLatLonInM(lat1,lon1,lat2,lon2) # find the distance between the POI and image coords.
						if distance <= flight_parameter:
							images.append(file_name)

		row[3] = images # assign third column of the row to images
		writer.writerow(row) # write the row into the csv file
		images.clear()

output_file.close() #close the output file
csvfile.close() # close the assests.csv file.


