# !/usr/bin/env python
# title           :BasicReadout.py
# description     :This file reads data from multimeter and writes to a file in disk
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
import sys
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

## Set header information
# set to 1 if the calibrator paddle is on
calibrator_boolean = 1
# angle of the horn form the horizontal perp to support axis
angle_perp = "90"
# angle of the horn form the horizontal along the support axis
angle_par = "20"
# temperatures in celcius
temperatureOutside = "14.0"
temperatureCalibrator = "-50"
weather = "very clear"
units  = "nanoWatt"

# =========================
# Make Header and File Name
# =========================
if calibrator_boolean:
    # where the horn was pointing
    looking = "Calibrator paddle"
    # was the calibrator in front
    calibrator = "YES"
else:
    looking = "Sky"
    calibrator = "NO"

date = time.strftime("%Y-%m-%d_%H:%M:%S")
duration_str = str(duration)

title = path + date + extension
# Create header for the file with all the information
# The header has 8 lines all satrting with #
header = "{0}\nDuration (in s): {7}" \
         "\nPointing Position of the Horn: {1}" \
         "\nAngle pointing (from horizontal perpendicular to supporting axis): {2}" \
         "\nAngle pointing (from horizontal parallel to supporting axis): {8}" \
         "\nCalibrator used: {3}" \
         "\nTemperature Outside (in celcius): {4}" \
         "\nTemperature of the calibrator (in celcius): {5}" \
         "\nWeather: {6}"\
         "\nUnits: {9}".format(
            title, looking, angle_perp, calibrator, temperatureOutside, temperatureCalibrator, weather, duration_str, angle_par, units)


data = []
# ===========
# Read Data
# ===========

# Create a new multimeter of the class Readout to read data
multimeter = Readout.Readout()

try:
    # printProgress(0, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)

    # Read for the duration set
    data = multimeter.read_loop(duration)

finally:
    # CTRL-C is pressed while reading or writing the data
    multimeter.close()

    # ============
    # Write Data
    # ============
    print('Writing data')
    np.savetxt(title, data, header=header)
    # printProgress(10, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)
    print('\a')
    print('Data written in file {0}'.format(title))
    sys.exit()
