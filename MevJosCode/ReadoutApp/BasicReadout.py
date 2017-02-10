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

#import ReadoutDebug as Rd
import Readout as Rd
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

# Set the path and name for the file where the data will be wirtten
# the file name will be of the form: path+"%Y-%m-%d_%H:%M:%S"+extension
# e.g "./Data/2016-11-10_10:20:50_Readout.txt"
# the extension must be a .txt file

fields = ('Duration in (s)', 'Path', 'Extension', 'Using Calibrator (1 for yes, 0 for No)',
          'Angle of the horn from horizontal perpendicular to support axis',
          'Angle of the horn from horizontal parallel to support axis', 'Temperature outside',
          'Temperature of the Calibrator', 'Weather', 'Units of reading', 'Comments')

defaultVal = ['60', './Data/', '_Readout.txt', '1', '90', '20', '14.0', '-50', 'very clear', 'nanoWatt', '']
data = []
title = ''
multimeter = Rd.Readout()
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


def makeheader(entries):
    entval = []
    for entry in entries:
        entval.append(entry.get())
    print(entval)

    calibrator_boolean = bool(entval[3])
    duration = int(entval[0])

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

    global title
    title = entval[1] + date + entval[2]
    return duration


def record(entries):
    duration = makeheader(entries)
    # Create a new multimeter of the class Readout to read data
    # global multimeter
    # multimeter = Rd.Readout()
    print('Reading Data...')
    # Read for the duration set
    global data
    data = multimeter.read_loop(duration)
    writefile()


def writefile():
    global multimeter
    multimeter.close()
    print('Writing data...')
    np.savetxt(title+'.txt', data)
    mean_temp = np.mean(data[:, 2])
    mean_volt = np.mean(data[:, 1])
    err_temp = spy.sem(data[:, 2])
    err_volt = spy.sem(data[:, 1])
    with open('./Data/Data_Sheet.csv', 'a') as csvfile:
        fieldnames = ['Duration (in s)', 'Pointing Position of the Horn',
                      'Angle pointing (from horizontal perpendicular to supporting axis)',
                      'Angle pointing (from horizontal parallel to supporting axis)', 'Calibrator used',
                      'Temperature Outside (in celcius)', 'Weather', 'Units', 'Mean Temperature', 'Temperature Error',
                      'Mean Voltage', 'Voltage Error']
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        # only necessary the first run
        writer.writerow({'Duration (in s)': duration_str, 'Pointing Position of the Horn': looking,
                         'Angle pointing (from horizontal perpendicular to supporting axis)': angle_perp,
                         'Angle pointing (from horizontal parallel to supporting axis)': angle_par,
                         'Calibrator used': calibrator, 'Temperature Outside (in celcius)': temperatureOutside,
                         'Weather': weather, 'Units': units, 'Mean Temperature': mean_temp,
                         'Temperature Error': err_temp, 'Mean Voltage': mean_volt, 'Voltage Error': err_volt})

    print('Data written in file {0}'.format(title))


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
