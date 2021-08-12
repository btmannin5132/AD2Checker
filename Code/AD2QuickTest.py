"""
compilation of the Supply, DIO and Waveform checks

Ben Manning 
Purdue ECE

07/20/2021
"""


from ctypes import *
from dwfconstants import *
import sys
import time

from AD2SupplyCheck import supplyCheck
from AD2DigitalCheck import digCheck
from AD2WaveCheck import waveCheck

global dwf
global hdwf
global dwRead
hdwf = c_int()
dwRead = c_uint32()
dwf = cdll.dwf



def close():
    dwf.FDwfDeviceClose(hdwf)

if __name__ == '__main__': 
    t = time.time()
    print("------------------------------------")
    print("")
    print("Running Supply Check...")
    supplyCheck()
    print("------------------------------------")
    print("")
    print("Running Wave Check on W1...")
    print("Change 1+ to W1")
    input("Press Enter When Ready")
    waveCheck(0)
    print("------------------------------------")
    print("")
    print("Running Wave Check on W2...")
    print("Change 1+ to W2")
    input("Press Enter When Done")
    waveCheck(1)

    print("------------------------------------")
    print("")
    print("Running Digital Check...")
    digCheck()
    print("------------------------------------")
    print("")

    close()
    dt = time.time() - t
    print("Test time: " + str(dt) + " seconds")



