import os
from struct import *
import struct
import numpy as np
import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog
from tkinter import *


header_struct = struct.Struct('<HBBHBBBBHi')
finishedList = []

echoIntensitiesL = []
echoIntensitiesR = []
imgL = []
imgR = []

i = 0
count = 0
directory = 'JSF-Processing/Sidescans/'
prediction = 0
account = 0

# OPTIONAL CAN ISNTEAD USE THE NORMAL DIRECTORY VARIABLE
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
directory = filedialog.askdirectory()

for filename in os.listdir(directory):
    if filename.endswith('.JSF'):
        prediction = 0
        i = 0
        with open(os.path.join(directory, filename), 'rb') as f:
            data = f.read()
            while prediction <= len(data):
                if prediction + 16 >= len(data):
                    break
                f.seek(i)
                header = f.read(header_struct.size)
                marker, protocalVersion, sessionID, messageType, cmdType, subSysNum, channel, \
                seqNum, reserved, msgSize = header_struct.unpack(header)

                # print(marker)
                if marker == 5633:
                    if protocalVersion == 14:
                        if(messageType > 2112):
                            pass
                        else:
                            
                            prediction = i + msgSize + 16
                            # i = prediction
                            # count +=1

                            if(messageType == 80) and subSysNum == 20:
                                account += 1
                                if channel == 0:
                                    j = i + 240 + 16
                                    echoIntensitiesL = []
                                    while j <= prediction:
                                        try: 
                                            val = struct.unpack('<h', data[j:j+2])[0]
                                            j += 2
                                            if val * 15 >= 28881:
                                            # if val * 15 >= 20000:
                                                val = 24881
                                                # pass
                                            else:
                                                val *= 15 
                                            echoIntensitiesL.append(val)
                                        except:
                                            break
                                if channel == 1:
                                    j = i + 240 + 16
                                    echoIntensitiesR = []
                                    while j <= prediction:
                                        try: 
                                            val = struct.unpack('<h', data[j:j+2])[0]
                                            j += 2
                                            if val * 15 >= 24881:
                                                val = 24881
                                            else:
                                                val *= 15
                                            echoIntensitiesR.append(val)
                                        except:
                                            break
                                msgCounter = 0
                                dataPoint = 0
                            i = prediction
                            count += 1
                            imgL.append(echoIntensitiesL)
                            imgR.append(echoIntensitiesR)


            print(f"finished file : {filename}")
            finishedList.append(filename)
            print(f"Count : {count}")
            print(f"Msg 80 count: {account}")
            print(np.unique(echoIntensitiesL))
            f.close()
        break
plt.subplot(1,2,1)
imgnew = []
for thing in imgL:
    if len(thing) == 7801:
        imgnew.append(thing)
plt.imshow(np.fliplr((np.array(imgnew)).T), cmap='pink', vmin= 500, vmax = 24881)
# plt.imshow(np.fliplr((np.array(imgnew)).T), cmap='pink', vmin= 0, vmax = 24881)
# plt.title("Port")
plt.subplot(1,2,2)
imgnew = []
for thing in imgR:
    if len(thing) == 7801:
        imgnew.append(thing)
plt.imshow(np.fliplr((np.array(imgnew)).T),cmap='pink', vmin= 500, vmax = 24881)
# plt.title("Startboard")
splitup = filename.split(".")
# filename = splitup[0] + "_PORT_R" + ".png"
filename = splitup[0] + ".png"
plt.savefig(filename)
plt.show()



# TODO
# Maybe add percentages for the procesing section
# So that its not either multiplied or not but instead
# Sections that are darker get multiplied by a larger amount
# than sections that are already bright
# Hopefully this will help to see more detail