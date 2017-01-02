# !/usr/bin/env python
# title           :BasicReadoutApp.py
# description     :This program is used to read data from a connected multimeter
#                   and writing it to a file that is then saved
# author          :Adriana Perez Rotondo
# date            :2017/01/1
# version         :0.1
# usage           :python BasicReadoutApp.py
# notes           :
# python_version  :2.7.10
# ==============================================================================

import ReadoutDebug as Rd
import time
import numpy as np
import sys

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

# form fields
fields = ['Duration in (s)',
          'Path (use the absolute path)',
          'Extension (should be a .txt file)',
          'Using Calibrator (1 for yes, 0 for No)',
          'Angle of the horn from horizontal perpendicular to support axis (usually 90)',
          'Angle of the horn from horizontal parallel to support axis',
          'Temperature outside in celcius',
          'Temperature of the Calibrator in celcius',
          'Weather',
          'Units of reading',
          'Comments']

# default values for the form's fields
defaultVal = ['60*2', '/Users/cosmology/Google Drive/Projects/radiometer/Data/', '_Readout.txt', '1', '90', '20', '14.0',
              '-50', 'very clear', 'nanoWatt', '']
# global variables
data = []
title = ''
multimeter = Rd.Readout()
header = ''
duration = 0

def makeform(r, f):
    # creates a form in the tk window r with the fields given by f
    entries = []
    i = 0
    for field in f:
        row = tk.Frame(r)
        lab = tk.Label(row, width=55, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        # put default value
        ent.insert(0, defaultVal[i])
        entries.append(ent)
        i += 1
    return entries


def makeheader(entries):
    # make the header for the output file using the form entries
    entval = []
    for entry in entries:
        entval.append(entry.get())
    # print(entval)

    calibrator_boolean = bool(entval[3])
    global duration
    duration = int(eval(entval[0]))

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

    # file name of the output file
    global title
    title = entval[1] + date + entval[2]

    # Create header for the file with all the information
    # The header has 9 lines all satrting with #
    global header
    header = "{0}\nDuration (in s): {7}" \
             "\nPointing Position of the Horn: {1}" \
             "\nAngle pointing (from horizontal perpendicular to supporting axis): {2}" \
             "\nAngle pointing (from horizontal parallel to supporting axis): {8}" \
             "\nCalibrator used: {3}" \
             "\nTemperature Outside (in celcius): {4}" \
             "\nTemperature of the calibrator (in celcius): {5}" \
             "\nWeather: {6}" \
             "\nUnits: {9}" \
             "\nComments: {10}".format(
        title, looking, entval[4], calibrator, entval[6], entval[7], entval[8], duration_str,
        entval[5], entval[9], entval[10])



def record(entries):
    # record data from the multimeter
    makeheader(entries)
    # Create a new multimeter of the class Readout to read data
    # global multimeter
    # multimeter = Rd.Readout()
    print('Reading Data...')
    # Read for the duration set
    global data
    data = multimeter.read_loop(duration)
    # write the data to the output file and save
    writefile()


def writefile():
    # writes header, data to the file with filename title and saves it
    global multimeter
    # close multimeter
    multimeter.close()
    print('Writing data...')
    try:
        np.savetxt(title, data, header=header)
    except IOError:
        print('Path not found')
        #tk.Message(root,text='Path not found')
        return
    print('Data written in file {0}'.format(title))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Multimeter Measurments')
    # size of window
    root.geometry("900x500")
    # make the form
    ents = makeform(root, fields)
    try:
        # record data when Return key is entered
        root.bind('<Return>', (lambda event, e=ents: record(e)))
        # create button to start measuring
        b1 = tk.Button(root, text='Start Measurement', command=(lambda e=ents: record(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
    except EOFError:
        # CTRL-C is pressed while reading or writing the data
        writefile()
        root.quit()
        sys.quit()
    except IOError:
        print('Path not found')
    # b2 = tk.Button(root, text='Stop', command=(lambda e=ents:writefile()))
    # b2.pack(side=tk.LEFT, padx=5, pady=5)
    # button to quit
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
