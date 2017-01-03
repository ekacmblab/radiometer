# EKA Radiometer Lab

## Synopsis
This project contains the files necessary to read data from a multimeter connected to the computer. 

## Contents
- **Readout.py** defines a multimeter class to get power measurements from the radiometer.
- **BasicReadout.py** reads data from multimeter for a set amount of time and saves data in a .txt file
- **BasicReadoutApp.py** Makes user interface to read data from multimeter for a set duration
- **setup.py** setup file to create OS X application from BasicReadoutApp.py
- **cmb.icns** icon for OS X app

## Setup Instructions
This section describes how to setup the OS X app based on BasicReadoutApp.py. If you don't want to create it you can run directly BasicReadout.py or BasicReadoutApp.py as explained in the Running instructions. 

For more information, this [tutorial](https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/) explains how to make an application with py2app.

- Open Terminal
- Install py2app (it might be necessary to use python3 to use py2app) check python version with the command `$ python version`

        $ pip install py2app
- Build app in alias mode

        $ python setup.py py2app -A

 If you are using anaconda installed python you have to edit PyRuntimeLocations field in Info.plist. Check if you are using anaconda python with the python command `$ which python` if the path contains an anaconda directory you should perform the next step. 
- Open Info.plist

        $ open dist/BasicReadoutApp.app/Contents/Info.plist
        
- Change name of file in `Item 1` of `PyRuntimeLocations` from `libpython3.5.dylib` to `libpython3.5m.dylib` (you just need to add an m after the 5)
- Save and close Info.plist

## Running instructions

### For OS X application

- Check that the multimeter is connected
- Open the BasicRedoutApp.app application using Finder or from the terminal found in folder `dist/`
- Fill in the different fields. Make sure the path is correct
- Press Start Measurement button

### For BasicRedoutApp.py (with user interface)

- Check that the multimeter is connected
- Open terminal 
- Run BasicReadoutApp.py

        $ python BasicReaoutApp.py

### For BasicReadout.py (no user interface)

- Check that the multimeter is connected
- Open BasicReadout.py 
- Set the preset variables duration, path and extension, angles, calibrator boolean, temperatures and weather, units 
- Run BasicReadout.py
        
        $ python BasicReadout.py

## Contributors

- Max Abitbol
- Alexander Leuning
- Adriana Perez Rotondo