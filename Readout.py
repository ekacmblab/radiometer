import numpy as np
import time
import visa

class Readout():
    def __init__(self):
        rm = visa.ResourceManager()
        self.multimeter = rm.open_resource('USB0::0x0957::0x0618::MY52210065::INSTR')
        self.multimeter.write("CONF:VOLT:DC:RANG 1")
        return

    def trigger(self,trigger_mode):
        self.multimeter.write("TRIG:SOUR "+trigger_mode)
        return

    def read(self):
        return self.multimeter.query_ascii_values("READ?")[0]

    def readLoop(self,duration):
        self.trigger("IMM")
        data = []
        t = []
        t1 = time.time()
        while time.time()-t1<=duration:
            t.append(time.time())
            data.append(self.read())
        self.trigger("BUS")
        combined_data = np.column_stack((t, data))
        return combined_data
