from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import math

def getDistanceFromLatLonInM(lat1,lon1,lat2,lon2): #haversine formula
	
	R = 6371; #Radius of the earth in km
	dLat = math.radians(lat2-lat1)  # convert degree to radians
	dLon = math.radians(lon2-lon1) 	# covert degree to radians
	a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
	d = R * c * 1000; # Distance in metres
  	
	return d

def get_exif_data(image):
	'''fucntion to return info about meta data of the image.
		special attention has been paid to GPSInfo which helps to get data about latitude, longitude and references.
	'''

	exif_data = {}
	meta_data = image._getexif()
    
	if meta_data:
		for key, value in meta_data.items():
	    	#print(key)
			decoded_key = TAGS.get(key, key)  #it is used to decode the key .
	    	#print(str(key) + " " + decoded_key + " " + str(value))
	    	#print(str(key) + " " + decoded_key) # prints the key and its decoded key.--> used for learning
			if decoded_key == "GPSInfo":
				gps_data = {} # a dictionary to store info about gps data of image
				for idx in value:
					#print(idx) #value ranges from 0 to 6.
					sub_decoded_key = GPSTAGS.get(idx, idx) # it is used to decode the key.
					#print(sub_decoded_key) # attributes like latilude, longitude , altitude and their references.
					gps_data[sub_decoded_key] = value[idx]

				exif_data[decoded_key] = gps_data
			else:
				exif_data[decoded_key] = value
    
	return exif_data

def convert_to_degrees(value):
	"""function to convert the GPS coordinates to degrees in float type"""
	degree = float(value[0][0]) / float(value[0][1])
	minutes = float(value[1][0]) / float(value[1][1])
	seconds = float(value[2][0]) / float(value[2][1])

	return degree + (minutes / 60.0) + (seconds / 3600.0)

def get_lat_lon(exif_data):

	"""Returns the latitude and longitude from the provided exif_data"""
	lat = None
	lon = None
	gps_latitude = None
	gps_latitude_ref = None
	gps_longitude = None
	gps_longitude_ref = None

	if "GPSInfo" in exif_data:		
		gps_info = exif_data["GPSInfo"]

		gps_latitude = gps_info["GPSLatitude"]
		gps_latitude_ref = gps_info["GPSLatitudeRef"]
		gps_longitude = gps_info["GPSLongitude"]
		gps_longitude_ref = gps_info["GPSLongitudeRef"]

		if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
			lat = convert_to_degrees(gps_latitude)
			if gps_latitude_ref != "N":                     
				lat = 0 - lat

			lon = convert_to_degrees(gps_longitude)
			if gps_longitude_ref != "E":
				lon = 0 - lon

	return lon, lat

'''
if __name__ == "__main__":
    image = Image.open("/home/jarvis/Desktop/software_dev/images/DJI_0004.JPG")
    exif_data = get_exif_data(image)
    #print(exif_data)
    print(get_lat_lon(exif_data))
'''
