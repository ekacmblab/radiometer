# !/usr/bin/env python
# title           :Readout.py
# description     :This file creates a class for a Agilent 34405A 5 1/2 Digit Multimeter
# author          :Adriana Perez Rotondo
# date            :2016/11/11
# version         :0.1
# usage           :import Readout
#                  r = Readout.Readout()
# notes           :
# python_version  :2.7.10
# ==============================================================================
"""This code creates a class for a Agilent 34405A 5 1/2 Digit Multimeter
and basic functions to read from the multimeter"""

import numpy as np
import time
import visa
from ProgressBar import printProgress
import random


class Readout():
    """This class creates a connection with the multimeter and has methods to read data form it

    """

    def __init__(self):
        print('Created')

    def close(self):
        print('close')

    def read_loop(self, duration):
        """Reads form multimeter for a given duration and returns an array with the time and value read for all readings

            Usually around 8 values are read per second

                :param duration: duration in seconds of the read
                :return: data read in array with time in seconds since the epoch and value read
        """
        # Trigger "IMM"
        data = []
        t = []
        try:
            t1 = time.time()            # start time
            i = 0
            # print(duration/10)
            # printProgress(i, duration/10, prefix='Progress reading data:', suffix='Complete', barLength=100)
            while time.time() - t1 <= duration:
                # If the time from the beggining is a multiple of 10....
                if (int(time.time())-int(t1)) % 10 == 0:
                    # print progressBar
                    i += 1
                    # printProgress(i, duration/10, prefix='Progress reading data:', suffix='Complete', barLength=100)
                t.append(time.time())
                data.append(self.read())
        except KeyboardInterrupt:
            print('Keyboard interrupt. Exiting...')
        finally:
            # when reading ends set trigger to "BUS"
            combined_data = np.column_stack((t, data))
            return combined_data


    def read(self):
        """ reads form multimeter and returns the data read
        -**return** and **return types**
            :return: returns the read data
        """
        # read from multimeter (automatically switches mode to "IMM")
        return random.random()
