import os
from struct import *
import struct
import numpy as np
import matplotlib.pyplot as plt
import time



header_struct = struct.Struct('<HBBHBBBBHi')
finishedList = []

echoIntensitiesL = []
img = []

i = 0
count = 0
directory = 'JSF-Processing/Sidescans/'
prediction = 0
account = 0
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

                            if(messageType == 80) and channel == 0 and subSysNum == 20:
                                echoIntensitiesL = []
                                account += 1
                                msgCounter = 0
                                dataPoint = 0
                                j = i + 240 + 16
                                # k = msgSize - 240 - 16
                                while j <= prediction:
                                    try: 
                                        val = struct.unpack('<h', data[j:j+2])[0]
                                        # if val > 0:
                                        #     print(j, val)
                                        j += 2
                                        # if val == 0:
                                            # val +=?
                                        # val +=2
                                        if val * 15 >= 24881:
                                            val = 24881
                                        else:
                                            val *= 15
                                        echoIntensitiesL.append(val)
                                    except:
                                        break
                                    # while msgCounter <= 16:
                                    #     dataPoint = dataPoint + data[j + msgCounter]
                                    #     msgCounter += 1
                                    # if(dataPoint != 0):
                                    #     print(f"Data point : {dataPoint}")
                                    #     break
                                    # echoIntensitiesL.append(dataPoint)
                                    # j += 16
                            i = prediction
                            count += 1
                            img.append(echoIntensitiesL)


            print(f"finished file : {filename}")
            finishedList.append(filename)
            print(f"Count : {count}")
            print(f"Msg 80 count: {account}")
            print(np.unique(echoIntensitiesL))
            f.close()
        break
imgnew = []
for thing in img:
    if len(thing) == 7801:
        imgnew.append(thing)
plt.imshow(np.fliplr((np.array(imgnew)).T), cmap='pink')
splitup = filename.split(".")
filename = splitup[0] + "_PORT_L" + ".png"
plt.savefig(filename)
# plt.imshow(np.fliplr((np.array(imgnew)).T), cmap='copper')
plt.show()
# print(f"\n\nTotal Count : {count}")
# print(f"Finished List : {finishedList}")