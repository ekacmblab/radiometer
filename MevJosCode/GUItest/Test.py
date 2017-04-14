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
duration = []
date = time.strftime("%Y-%m-%d_%H:%M:%S")
multimeter = Readout.Readout()
entval = []

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
    duration_str.append(str(duration))
    title = entval[1] + date + entval[2]
    print('Reading Data...')
    data = multimeter.read_loop(duration)




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
        root.quit()
        sys.quit()
    # b2 = tk.Button(root, text='Stop', command=(lambda e=ents:writefile()))
    # b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

print(duration[0])
print (duration_str[0])