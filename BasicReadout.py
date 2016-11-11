import Readout as r
import time
import numpy as np

"""" """
#=========
# Presets
#=========

# Duration of the read
duration = 5*60

# Set the path and name for the file where the data will be wirtten
# the file name will be of the form: path+"%Y-%m-%d_%H:%M:%S"+extension
# e.g "./Data/2016-11-10_10:20:50_Readout.txt"
# the extension must be a .txt file
path = "./Data/"
extension = "_Readout.txt"

# Set heading information
date = time.strftime("%Y-%m-%d_%H:%M:%S")
# where the horn was pointing
looking = "East window Pupin 605"
# angle of the horn
angle = "80"
# temperatures
temperatureOutside = ""
temperatureCalibrator = ""
weather = "clear"
duration = str(duration)
# was the calibrator in front
calibrator = "Yes"

#===========
# Read Data
#===========

# Create a new multimeter of the class Readout to read data
multimeter = r.Readout()

# Read for the duration set
read = multimeter.readLoop(duration)

#============
# Write Data
#============

title = path + date + extension

# Create header for the file with all the information
# The header has 8 lines all satrting with #
header = "{0}\nDuration: {7}\nPointing Position of the Horn: {1}\nAngle pointing: {2}\nCalibrator used: " \
         "{3}\nTemperature Outside: {4}\nTemperature of the calibrator: {5}\nWeather: {6}".format(
    title, looking, angle, calibrator, temperatureOutside,temperatureCalibrator,weather,duration)

np.savetxt(title,read,header=header)

