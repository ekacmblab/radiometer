import Readout as r
import time
import numpy as np
import pylab as pl

duration = 5*60


multimeter = r.Readout()

read = multimeter.readLoop(duration)

date = time.strftime("./Data/%Y-%m-%d_%H:%M:%S")
looking = "East window Pupin 605"
angle = "80"
temperatureOutside = ""
temperatureCalibrator = ""
weather = "clear"
duration = str(duration)
calibrator = "Yes"

timestr = date+"_Readout.txt"
np.savetxt(timestr,read)

