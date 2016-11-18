# !/usr/bin/env python
# title           :BasicReadout.py
# description     :This file reads data fro multimeter and writes to a file in disk
# author          :Adriana Perez Rotondo
# date            :2016/11/11
# version         :0.1
# usage           :python BasicReadout.py
# notes           :
# python_version  :2.7.10
# ==============================================================================

import Readout
import time
import numpy as np
from ProgressBar import printProgress

# =========
# Presets
# =========

# Duration of the read
duration = 1*60

# Set the path and name for the file where the data will be wirtten
# the file name will be of the form: path+"%Y-%m-%d_%H:%M:%S"+extension
# e.g "./Data/2016-11-10_10:20:50_Readout.txt"
# the extension must be a .txt file
path = "./Data/"
extension = "_Readout.txt"

# Set heading information
date = time.strftime("%Y-%m-%d_%H:%M:%S")
# where the horn was pointing
looking = "Calibration Paddle"
# angle of the horn form the horizontal perp to support axis
angle_perp = "90"
# angle of the horn form the horizontal along the support axis
angle_par = "90"
# temperatures
temperatureOutside = "14"
temperatureCalibrator = "room temp"
weather = "very clear. windy"
duration_str = str(duration)
# was the calibrator in front
calibrator = "Yes"

# ===========
# Read Data
# ===========

# Create a new multimeter of the class Readout to read data
multimeter = Readout.Readout()

# Read for the duration set
<<<<<<< HEAD
data = multimeter.read_loop(duration)
=======
read = multimeter.read_loop(duration)
#read = np.random.rand(10)
>>>>>>> 3e434df1989ca4ae0ce36b44e7bc556d5338223b

# ============
# Write Data
# ============

title = path + date + extension

printProgress(0, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)

# Create header for the file with all the information
# The header has 8 lines all satrting with #
header = "{0}\nDuration (in s): {7}" \
         "\nPointing Position of the Horn: {1}" \
         "\nAngle pointing (from horizontal perpendicular to supporting axis): {2}" \
         "\nAngle pointing (from horizontal parallel to supporting axis): {8}" \
         "\nCalibrator used: {3}" \
         "\nTemperature Outside (in celcius): {4}" \
         "\nTemperature of the calibrator (in celcius): {5}" \
         "\nWeather: {6}".format(
            title, looking, angle_perp, calibrator, temperatureOutside, temperatureCalibrator, weather, duration_str, angle_par)

<<<<<<< HEAD
np.savetxt(title, data, header=header)
=======
printProgress(7, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)

np.savetxt(title, read, header=header)

printProgress(10, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)
>>>>>>> 3e434df1989ca4ae0ce36b44e7bc556d5338223b
