"""
AD2 Digital IO Check

Wire 
D0 to D8
D1 to D9
D2 to D10
...

EAch test outputs 16 bits
Pin order:

15 14 13 ... 3 2 1 0

Ben Manning
Purdue ECE

07/20/2021

"""

from ctypes import *
from dwfconstants import *
import sys
import time

dwf = cdll.dwf
hdwf = c_int()
dwRead = c_uint32()

def digCheck():

    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    hdwf = c_int()
    dwRead = c_uint32()

    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    #print("DWF Version: "+str(version.value))

    #print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        print("failed to open device")
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        quit()


    #Check D0-D7 as outputs first
    dwf.FDwfDigitalIOOutputEnableSet(hdwf, c_int(0x00FF)) 
    # set value on enabled IO pins

    #Test1
    #all 1
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x00FF)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "1111111111111111"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 1 Passed")
    else:
        print("Test 1 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))


    #Test2
    #alternate
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x0055)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "0101010101010101"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 2 Passed")
    else:
        print("Test 2 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))

    #Test3
    #reverse alternate
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x00aa)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "1010101010101010"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 3 Passed")
    else:
        print("Test 3 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))

    #Test4
    #All 0
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x0000)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "0000000000000000"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 4 Passed")
    else:
        print("Test 4 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))

    #Swap Outputs
    dwf.FDwfDigitalIOOutputEnableSet(hdwf, c_int(0xFF00)) 

    #Test5
    #all 1
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0xFF00)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "1111111111111111"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 5 Passed")
    else:
        print("Test 5 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))


    #Test6
    #alternate
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x5500)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "0101010101010101"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 6 Passed")
    else:
        print("Test 6 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))

    #Test7
    #reverse alternate
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0xaa00)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "1010101010101010"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 7 Passed")
    else:
        print("Test 7 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))

    #Test8
    #All 0
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(0x0000)) 
    time.sleep(1)
    dwf.FDwfDigitalIOStatus (hdwf) 
    # read state of all pins, regardless of output enable
    dwf.FDwfDigitalIOInputStatus(hdwf, byref(dwRead)) 
    expected = "0000000000000000"
    #print(bin(dwRead.value)[2:].zfill(16))
    if str(bin(dwRead.value)[2:].zfill(16)) == expected:
        print("Test 8 Passed")
    else:
        print("Test 8 Fail")
        print("Expected output: " + expected)
        print("Acutal: " + str(bin(dwRead.value)[2:].zfill(16)))
    dwf.FDwfDeviceClose(hdwf)



def close():
    dwf.FDwfDeviceClose(hdwf)
