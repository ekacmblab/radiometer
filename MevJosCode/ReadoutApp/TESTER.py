# !/usr/bin/env python
# title           :BasicReadout.py
# description     :This file reads data from multimeter and writes to a file in disk
# author          :Adriana Perez Rotondo
# editor	      :Joseph Dominicus Lap
# date            :2017/10/02
# version         :0.1.3
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
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk


# =========
# Presets
# =========
defaultVal = ['60', './Data/', '_Readout.txt', '1', '90', '20', '14.0', '-50', 'very clear', 'nanoWatt', '']
data = []
title = ''
multimeter = Readout.Readout()
header = ''

def makeform(r, f):
    entries = []
    i = 0
    for field in f:
        row = tk.Frame(r)
        lab = tk.Label(row, width=50, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        ent.insert(0, defaultVal[i])
        entries.append(ent)
        i += 1
    return entries



# Set the path and name for the file where the data will be written
# the file name will be of the form: path+"%Y-%m-%d_%H:%M:%S"+extension
# e.g "./Data/2016-11-10_10:20:50_Readout.csv"
# the extension must be a .csv file
path = "./Data/"
extension = "_Readout"

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

    #Appends a .csv with all the inputted data

    print('Writing data')
    with open('./Data/Data_Sheet.csv', 'a') as csvfile:
        fieldnames = ['Duration (in s)', 'Pointing Position of the Horn', 'Angle pointing (from horizontal perpendicular to supporting axis)', 'Angle pointing (from horizontal parallel to supporting axis)','Calibrator used','Temperature Outside (in celcius)','Weather','Units','Mean Temperature','Temperature Error','Mean Voltage','Voltage Error']
        writer = csv.DictWriter(csvfile, delimiter=',' ,fieldnames=fieldnames)
        #writer.writeheader()
        #only necessary the first run
        writer.writerow({'Duration (in s)':duration_str, 'Pointing Position of the Horn':looking, 'Angle pointing (from horizontal perpendicular to supporting axis)':angle_perp, 'Angle pointing (from horizontal parallel to supporting axis)':angle_par, 'Calibrator used':calibrator, 'Temperature Outside (in celcius)':temperatureOutside, 'Weather':weather, 'Units': units, 'Mean Temperature': mean_temp, 'Temperature Error': err_temp, 'Mean Voltage': mean_volt, 'Voltage Error': err_volt})

        #np.savetxt(title, data, header=header)
    # printProgress(10, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)
    print('\a')
    print('Data written in file {0}'.format(title))
    sys.exit()

# ==================
# Form
# ==================

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Multimeter Measurments')
    root.geometry("800x500")
    ents = makeform(root, fields)
    try:
        root.bind('<Return>', (lambda event, e=ents: record(e)))
        b1 = tk.Button(root, text='Start Measurement', command=(lambda e=ents: record(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
    except EOFError:
        # CTRL-C is pressed while reading or writing the data
        writefile()
        root.quit()
        sys.quit()
    # b2 = tk.Button(root, text='Stop', command=(lambda e=ents:writefile()))
    # b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
