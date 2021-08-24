"""
AD2 Power Supply Check

Uses Input 1 to check + supply
1+ to V+, 1- to GND

Uses Input 2 to check - supply
2+ to V-, 2- to GND

If percent error is High, check both supply and input

Ben Manning
Purdue ECE

Last Edit: 07/20/2021
"""


from ctypes import *
from dwfconstants import *
import time
import sys
import math

dwf = cdll.dwf
hdwf = c_int()

def close():
    dwf.FDwfDeviceClose(hdwf)

def supplyCheck():

    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    hdwf = c_int()


    #print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        print("failed to open device")
        quit()

    print("Device Opened")

    voltage1 = c_double()
    voltage2 = c_double()
    #setup Channels to read in supplies
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True)) 
    dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(0), c_double(0)) 
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(10)) 
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(10)) 
    dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(False))

    dwf.FDwfAnalogInStatus(hdwf, False, None) 
    sample = 5

    print("Checking Positive Supply, please switch ch 2+ to V+")
    input("Press enter when ready")

    for x in [5.0,0,.05,2.5,0,5.0]:
        # set up analog IO channel nodes
        # enable positive supply
        print("Checking + " + str(x) + "V")
        
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(True)) 
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(x)) 
        #dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(True)) 
        #dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(x*-1)) 
        dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))

        #Let supply stabilize
        time.sleep(.25)
        Vp = 0
       # Vn = 0
        for i in range(0, sample):
            dwf.FDwfAnalogInStatus(hdwf, False, None) 
            dwf.FDwfAnalogInStatusSample(hdwf, c_int(1), byref(voltage1))
            #dwf.FDwfAnalogInStatusSample(hdwf, c_int(1), byref(voltage2))
            Vp += voltage1.value
            #Vn += voltage2.value
            #print("Channel 1:  " + str(voltage1.value)+" V  || Channel 2:  " + str(voltage2.value)+" V")
            time.sleep(.25)
        VpAvg = Vp/sample
        if x == 0:
            print('Expected + Supply: {0:.4f} V || Measured + Supply: {1:.4f} V'.format(x,VpAvg))
        else:
            
            vpError = abs((abs(VpAvg)-x)/x)*100
            print('Expected + Supply: {0:.4f} V || Measured + Supply: {1:.4f} V || Error: {2:.4f} %'.format(x,VpAvg,vpError))
            if vpError < 3:
                print("Ok")
            else:
                print("Check Supply")
        print("")

    """
        VnAvg = Vn/sample
        vnError = abs((abs(VnAvg)-x)/(x+.01))*100
        print('Expected - Supply: {0:.4f} V || Measured - Supply: {1:.4f} V || Error: {2:.4f} %'.format(x*-1,VnAvg,vnError))
    """ 

    print("Checking Negative Supply, please switch ch 2+ to V-")
    input("Press enter when ready")

    for x in [5.0,0,.05,2.5,0,5.0]:
        # set up analog IO channel nodes
        # enable positive supply
        print("Checking - " + str(x) + "V")
        #dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(True)) 
        #dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(x)) 
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(True)) 
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(x*-1)) 
        dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))

        #Let supply stabilize
        #reduced for processing time
        time.sleep(.25)
        Vn = 0
       # Vn = 0
        for i in range(0, sample):
            dwf.FDwfAnalogInStatus(hdwf, False, None) 
            #dwf.FDwfAnalogInStatusSample(hdwf, c_int(1), byref(voltage1))
            dwf.FDwfAnalogInStatusSample(hdwf, c_int(1), byref(voltage2))
            Vn += voltage2.value
            #print("Channel 1:  " + str(voltage1.value)+" V  || Channel 2:  " + str(voltage2.value)+" V")
            time.sleep(.25)
        VnAvg = Vn/sample
        if x == 0:
            print('Expected - Supply: {0:.4f} V || Measured - Supply: {1:.4f} V '.format(x*-1,VnAvg))
        else:
            vnError = abs(((abs(VnAvg)-x)/x)*100)
            print('Expected - Supply: {0:.4f} V || Measured - Supply: {1:.4f} V || Error: {2:.4f} %'.format(x*-1,VnAvg,vnError))
            if vnError < 3:
                print("Ok")
            else:
                print("Check Supply")
        print("")


    dwf.FDwfAnalogIOEnableSet(hdwf, c_int(False)) 
    dwf.FDwfDeviceClose(hdwf)



if __name__ == '__main__':
    supplyCheck()

#supplyCheck()
#close()