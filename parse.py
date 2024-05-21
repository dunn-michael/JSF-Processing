import os
from struct import *
import struct
import numpy as np


header_struct = struct.Struct('<HBBHBBBBHi')
finishedList = []

echoIntensities = []

i = 0
count = 0
directory = 'JSF-Processing/Sidescans/'
prediction = 0
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

                            if(messageType == 80):
                                msgCounter = 0
                                dataPoint = 0
                                j = i + 240 + 16
                                k = msgSize - 240 - 16
                                while j <= prediction:
                                    while msgCounter <= 16:
                                        dataPoint = dataPoint + data[j + msgCounter]
                                        msgCounter += 1
                                    if(dataPoint != 0):
                                        print(f"Data point : {dataPoint}")
                                        break
                                    echoIntensities.append(dataPoint)
                                    j += 16
                            i = prediction
                            count += 1


            print(f"finished file : {filename}")
            finishedList.append(filename)
            print(f"Count : {count}")
            print(np.unique(echoIntensities))
            f.close()
print(f"\n\nTotal Count : {count}")
print(f"Finished List : {finishedList}")