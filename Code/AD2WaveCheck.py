"""
WaveCheck for AD2
Checks Sine, Square and Triangle waves
Gives expected and measured max and min values for each wave

Ben Manning
Purdue ECE

07/21/2021
"""

from ctypes import *
import time
from dwfconstants import *
import sys
import matplotlib.pyplot as plt
import numpy

dwf = cdll.dwf
hdwf = c_int()

def waveCheck(ch):
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    #print("Version: "+str(version.value))

    cdevices = c_int()
    dwf.FDwfEnum(c_int(0), byref(cdevices))
    #print("Number of Devices: "+str(cdevices.value))

    if cdevices.value == 0:
        print("no device detected")
        quit()

    #print("Opening first device")
    hdwf = c_int()
    dwf.FDwfDeviceOpen(c_int(0), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        print("failed to open device")
        quit()


    dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(ch), c_int(0), c_double(True)) 
    dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(ch), c_int(1), c_double(0.0)) 
    dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))

    time.sleep(1)

    print("Configure and start first analog out channel")
    dwf.FDwfAnalogOutEnableSet(hdwf, c_int(ch), c_int(1))
    dwf.FDwfAnalogOutFunctionSet(hdwf, c_int(ch), c_int(1)) #1 = sine, 2 = square, 3 = tri
    dwf.FDwfAnalogOutFrequencySet(hdwf, c_int(ch), c_double(1000))
    dwf.FDwfAnalogOutConfigure(hdwf, c_int(ch), c_int(1))

    print("Configure analog in")
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(1000000))
    print("Set range for all channels")
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(4))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(5000))

    print("")

    #print("Wait after first device opening the analog in offset to stabilize")
    time.sleep(1)

    print("Starting Sine acquisition...")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))



    sts = c_int()
    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    #print("   done")

    rg = (c_double*5000)()
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rg, len(rg)) # get channel 1 data
    #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg, len(rg)) # get channel 2 data

    dwf.FDwfAnalogOutReset(hdwf, c_int(0))

    i = 0
    mi = min(rg)
    while rg[i] != mi:
        i+=1
    ma = max(rg)
    #print(i)

    sineRg = rg[0:2000]
    print("SineMin: " + str(mi) + "V, Expected -1V")
    print("SineMax: " + str(ma) + "V, Expected 1V")
    dc = sum(sineRg)/len(sineRg)
    print("Sine DC: "+str(dc)+"V")
    #print(newRg[0])


    print("")

    #print("Configure and start first analog out channel")
    dwf.FDwfAnalogOutEnableSet(hdwf, c_int(ch), c_int(1))
    dwf.FDwfAnalogOutFunctionSet(hdwf, c_int(ch), c_int(2)) #1 = sine, 2 = square, 3 = tri
    dwf.FDwfAnalogOutFrequencySet(hdwf, c_int(ch), c_double(1000))
    dwf.FDwfAnalogOutConfigure(hdwf, c_int(ch), c_int(1))

    #print("Configure analog in")
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(1000000))
    #print("Set range for all channels")
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(4))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(5000))

    #print("Wait after first device opening the analog in offset to stabilize")
    time.sleep(1)

    print("Starting Square acquisition...")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))



    sts = c_int()
    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    #print("   done")

    rg = (c_double*5000)()
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rg, len(rg)) # get channel 1 data
    #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg, len(rg)) # get channel 2 data

    dwf.FDwfAnalogOutReset(hdwf, c_int(0))

    i = 0
    mi = min(rg)
    while rg[i] != mi:
        i+=1
    ma = max(rg)
    #print(i)

    SqRg = rg[0:2000]
    print("SquareMin: " + str(mi) + "V, Expected -1V")
    print("SquareMax: " + str(ma) + "V, Expected 1V")
    dc = sum(SqRg)/len(SqRg)
    print("Square DC: "+str(dc)+"V")
    #print(newRg[0])

    print("")

    #print("Configure and start first analog out channel")
    dwf.FDwfAnalogOutEnableSet(hdwf, c_int(ch), c_int(1))
    dwf.FDwfAnalogOutFunctionSet(hdwf, c_int(ch), c_int(3)) #1 = sine, 2 = square, 3 = tri
    dwf.FDwfAnalogOutFrequencySet(hdwf, c_int(ch), c_double(1000))
    dwf.FDwfAnalogOutConfigure(hdwf, c_int(ch), c_int(1))

    #print("Configure analog in")
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(1000000))
    #print("Set range for all channels")
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(4))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(5000))

    #print("Wait after first device opening the analog in offset to stabilize")
    time.sleep(1)

    print("Starting Triangle acquisition...")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))



    sts = c_int()
    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    #print("   done")

    rg = (c_double*5000)()
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rg, len(rg)) # get channel 1 data
    #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg, len(rg)) # get channel 2 data

    dwf.FDwfAnalogOutReset(hdwf, c_int(0))

    i = 0
    mi = min(rg)
    while rg[i] != mi:
        i+=1
    ma = max(rg)
    #print(i)

    TriRg = rg[0:2000]
    print("Triangle Min: " + str(mi) + "V, Expected -1V")
    print("TriangleMax: " + str(ma) + "V, Expected 1V")
    dc = sum(TriRg)/len(TriRg)
    print("Triangle DC: "+str(dc)+"V")
    #print(newRg[0])

    print("")

    dwf.FDwfAnalogIOEnableSet(hdwf, c_int(False)) 


   
    fig, axs = plt.subplots(3)
    fig.suptitle('Sine, Square and Triangle Plots from AD2')
    axs[0].plot(numpy.fromiter(sineRg, dtype = numpy.float))
    axs[1].plot(numpy.fromiter(SqRg, dtype = numpy.float))
    axs[2].plot(numpy.fromiter(TriRg, dtype = numpy.float))
    plt.draw()
    plt.show()
    dwf.FDwfDeviceClose(hdwf)

def close():
    dwf.FDwfDeviceClose(hdwf)


if __name__ == '__main__':
    print("Running Wave Check on W1...")
    waveCheck(0)
    print("------------------------------------")
    print("Change 1+ to W2")
    input("Press Enter When Done")
    print("")
    print("Running Wave Check on W2...")
    waveCheck(1)