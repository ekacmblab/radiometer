# !/usr/bin/env python
import serial
import time

class Thermometer:
    def __init__(self):
        self.thermo = serial.Serial('/dev/tty.usbserial', baudrate=9600, parity='O', bytesize=7,
                               stopbits=1, timeout=1)
        self.mname()
        x = self.tempstr()

    def mname(self):
        self.thermo.write("*IDN?\r\n")
        print self.strip_parity(self.thermo.read(100))

    def tempstr(self):
        self.thermo.write("KRDG?\r\n")
        time.sleep(0.05) 
        tempout = []
        while self.thermo.inWaiting():
            tempout.append(self.thermo.read(1)) 
        return self.strip_parity(tempout)
    
    def get_temp(self):
        data = self.tempstr() 
        return float(data.split('+')[-1].split('\r')[0])

    def strip_parity(self, x):
        result = []
        for k in x:
            result.append(chr(ord(k) & 0x7F))
        return ''.join(result)
    
	  
