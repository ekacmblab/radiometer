# !/usr/bin/env python
# title           :Readout.py
# description     :This file reads data from multimeter and writes to a .csv in disk
# author          :Joseph Dominicus Lap
# date            :2017/24/02
# version         :0.1
# usage           :python Readout.py
# notes           :To improve: mess with the fact that almost everything is made global.
# python_version  :2.7.10
# ==============================================================================

import Readout
import time
from scipy import stats as spy
import numpy as np
import csv
import sys
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk



# =============
# Define Things
# =============
data = []
date = time.strftime("%Y-%m-%d_%H:%M:%S")
multimeter = Readout.Readout()
entval = []
duration = []
title =[]

# ================
# Make Form
# ================

# Default Values
fields = ('Duration (in s)', 'Path', 'Extension',
          'Angle pointing (from horizontal perpendicular to supporting axis)',
          'Angle pointing (from horizontal parallel to supporting axis)',
          'Calibrator used','Temperature Outside (in celcius)',
          'Weather','Units','Comments')

defaultVal = ['60', './Data/', '_Readout.txt', '90', '0', '1', '14.0',  'very clear', 'nanoWatt', '']

# Creates a Form
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


def record(entries):
    for entry in entries:
        entval.append(entry.get())
    duration.append(int(entval[0]))
    title.append(entval[1] + date + entval[2])
    print('Reading Data...')






# ===================
# BULK of Program
# ===================


# Puts Proper Fields and calls CSV
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Multimeter Measurments')
    root.geometry("800x500")
    ents = makeform(root, fields)

    try:
        root.bind('<Return>', (lambda event, e=ents: record(e)))
        b1 = tk.Button(root, text='Start Measurement', command=(lambda e=ents: record(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        # CTRL-C is pressed while reading or writing the data
    except EOFError:
        sys.quit()
        root.quit()

    # b2 = tk.Button(root, text='Stop', command=(lambda e=ents:writefile()))
    # b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    # This is a shitty way of making the variables global
    duration = duration[0]
    duration_str =str(duration)
    title = title[0]

    try:
        # printProgress(0, 10, prefix='Progress writing data:', suffix='Complete', barLength=50)

        # Read for the duration set
        data = multimeter.read_loop(duration)

    finally:
        # CTRL-C is pressed while reading or writing the data
        multimeter.close()
        # Writes A Text File
        np.savetxt(title + '.txt', data)
        # Does some Data Analysis
        mean_temp = np.mean(data[:, 2])
        mean_volt = np.mean(data[:, 1])
        err_temp = spy.sem(data[:, 2])
        err_volt = spy.sem(data[:, 1])

        # Appends a .csv with all the inputted data
        print('Writing data')
        with open('./Data/Data_Sheet.csv', 'a') as csvfile:
            fieldnames = ['Duration (in s)', 'Angle pointing (from horizontal perpendicular to supporting axis)',
                          'Angle pointing (from horizontal parallel to supporting axis)', 'Calibrator used',
                          'Temperature Outside (in celcius)', 'Weather', 'Units', 'Mean Temperature',
                          'Temperature Error',
                          'Mean Voltage', 'Voltage Error', 'Comments']
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            # writer.writeheader()()
            # Above is only necessary the first run
            writer.writerow({'Duration (in s)': duration_str,
                             'Angle pointing (from horizontal perpendicular to supporting axis)': entval[3],
                             'Angle pointing (from horizontal parallel to supporting axis)': entval[4],
                             'Calibrator used': entval[5], 'Temperature Outside (in celcius)': entval[6],
                             'Weather': entval[7], 'Units': entval[8], 'Mean Temperature': mean_temp,
                             'Temperature Error': err_temp,
                             'Mean Voltage': mean_volt, 'Voltage Error': err_volt, 'Comments': entval[9]})

        print('\a')
        print('Data written in file {0}'.format(title))





