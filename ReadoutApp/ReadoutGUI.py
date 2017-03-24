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

import electronics as Rd
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

fields = ('Duration in (s)', 'Path', 'Extension', 'Using Calibrator (1 for yes, 0 for No)',
          'Angle of the horn from vertical', 'Weather', 'Units of reading', 'Comments')

defaultVal = ['10', './Data/', '_Readout.txt', '1', '0', 'very clear', 'nanoWatt', '']
multimeter = Rd.Readout()

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
    title = entval[1] + date + entval[2]
    header = "{0}\nDuration (in s): {0}" \
             "\nPointing Position of the Horn: {1}" \
             "\nAngle pointing (from vertical): {2}" \
             "\nCalibrator used: {3}" \
             "\nWeather: {4}" \
             "\nUnits: {5}" \
             "\nComments: {6}".format(duration_str, looking, entval[4], calibrator, entval[5], entval[6], entval[7])
    return duration, header, title

def record(entries):
    print('Reading Data...')
    duration, header, title = makeheader(entries)
    data = multimeter.read_loop(duration)
    writefile(title, data, header)
    return

def writefile(title, data, header):
    np.savetxt(title, data, header=header)
    print('Data written in file {0}'.format(title))
    return


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
        multimeter.close()
        root.quit()
        sys.quit()
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
    multimeter.close()
