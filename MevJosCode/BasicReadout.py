# !/usr/bin/env python
# title           :BasicReadout.py
# description     :This file reads data from multimeter and writes to a file in disk
# author          :Adriana Perez Rotondo
# editor	      :Joseph Dominicus Lap
# date            :2017/03/02
# version         :0.1.2
# usage           :python BasicReadout.py
# notes           :
# python_version  :2.7.10
# ==============================================================================

import Readout
import time
from scipy import stats as spy
import numpy as np
import sys
import csv
from ProgressBar import printProgress

# =========
# Presets
# =========

# Duration of the read in seconds
duration = 60

# Set the path and name for the file where the data will be wirtten
# the file name will be of the form: path+"%Y-%m-%d_%H:%M:%S"+extension
# e.g "./Data/2016-11-10_10:20:50_Readout.csv"
# the extension must be a .csv file
path = "./Data/"
extension = "_Readout.csv"

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
# Make File Name
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
    # Write and then Analyze Data
    # ============
    np.savetxt(title+'.txt', data)
    mean_temp = np.mean(data[:,2])
    mean_volt = np.mean(data[:,1])
    err_temp = spy.sem(data[:,2])
    err_volt = spy.sem(data[:,1])
    

    # ============
    # Make Clean CSV
    # ============
    print('Writing data')
    with open(title, 'wb') as csvfile:
	fieldnames = ['Duration (in s)', 'Pointing Position of the Horn', 'Angle pointing (from horizontal perpendicular to supporting axis)', 'Angle pointing (from horizontal parallel to supporting axis)','Calibrator used','Temperature Outside (in celcius)','Weather','Units','Mean Temperature','Temperature Error','Mean Voltage','Voltage Error']
 	writer = csv.DictWriter(csvfile, delimiter=',' ,fieldnames=fieldnames)
	writer.writeheader()

	#Writes a .csv with all the inputted data


	writer.writerow({'Duration (in s)':duration_str, 'Pointing Position of the Horn':looking, 'Angle pointing (from horizontal perpendicular to supporting axis)':angle_perp, 'Angle pointing (from horizontal parallel to supporting axis)':angle_par, 'Calibrator used':calibrator, 'Temperature Outside (in celcius)':temperatureOutside, 'Weather':weather, 'Units': units, 'Mean Temperature': mean_temp, 'Temperature Error': err_temp, 'Mean Voltage': mean_volt, 'Voltage Error': err_volt})

    	#np.savetxt(title, data, header=header)
    # printProgress(10, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)
    print('\a')
    print('Data written in file {0}'.format(title))
    sys.exit()
