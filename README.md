# Assignment_Code
As the name suggests, assets.py handles the case of finding images which are at a distance of <= 50m from the Point Of Interests (POIs) given in the assets.csv file.The value of flight parameter (i.e. 50) is not fixed, it is taken as a command line argument while running the script as it was written in the README.txt. For now the path of images folder is hard coded into the script but they can also be taken as command line argument.
Different modules have been imported in this scirpt for different purposes such as "os" to list all the files present in a directory,"csv" module to read and write into a csv file and etc.A module named "utility" has been imported in it for different functions such as getting exif data from image, get latitude and longitude info from that and find distance between coordinates. This module has been explained later.

The next module is video.py . The function of this module was similar to the asset.py .But here the coordiantes has to be read from a srt file.For this a module named 'pysrt' has been imported which helps in extracting the coordinates from the file.
One important thing to notice here was that for every second 1000 miliseconds should be there, which implies 10 consecutive readings from the srt file should be taken for one second as the readings are of the form 0-100,100-200,200-300....900-000 .
There is one special case for the first second where there are only 9 readings given.Reading 0-100 is missing there.This case has been handled in the code.

The last module is utility.py which uses PIL (Python Imaging Library) in it. This module contains the different functions such as extracting exif_data to get the meta data from the image, function to find distance between 2 pairs of latitude and longitude, function to get latitude & longitude value from the exif data of the image.This module has been used in the above 2 modules to find the exif data and calculate distances between 2 coordinates.


To run the modules -- 
Before running the modules,change the path of different files/folders according to your system.

python3 assets.py parameter
or 
python3 assets.py -- in this case flight parameter is initialized to 50

python3 video.py parameter
or 
python3 video.py -- in this case flight parameter is initialized to 35
