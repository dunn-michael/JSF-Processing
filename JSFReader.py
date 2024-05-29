import os
from struct import *
import struct
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *
import math
# from histManipulation import *

def setupGraph(listName):
    imgnew = []
    for thing in listName:
        # print(len(thing))
        if len(thing) == 15602:
            # Value if graphing single graphs instead of combined
        # if len(thing) == 7801:
            imgnew.append(thing)
    array = np.array(imgnew)
    
    # array = equalize_histogram(array, "gaussian")
    # plt.title("Sonar map")
    # plt.subplot(3,1,1)
    plt.imshow(np.fliplr((array).T), cmap='pink', vmin= 0, vmax = 24881)
    # plt.title("Graph of single swath")
    # plt.subplot(3,1,2)
    # plt.plot(array[1])
    # plt.title("Histogram")
    # plt.subplot(3,1,3)
    # plt.hist(array[1], bins=200, color='skyblue', edgecolor='black')
    # plt.title(channel)
    # equ


def main():
    
    header_struct = struct.Struct('<HBBHBBBBHi')
    finishedList = []

    echoIntensitiesL = []
    echoIntensitiesR = []
    imgL = []
    imgR = []
    img = []
    totalR = []
    totalL = []
    prevLong = 0
    prevLat = 0
    same = 0
    skip = False

    i = 0
    count = 0
    directory = 'Sidescans/'
    account = 0
    
    # This is the absorption coefficient use for TVG
    # alpha = 4.9
    alpha = 7.5
    # alpha = 

    # TODO
    # UNCOMMENT LATER
    # OPTIONAL CAN ISNTEAD USE THE NORMAL DIRECTORY VARIABLE
    # tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    # directory = filedialog.askdirectory()

    # Looks at your directory and finds .JSF files to open and parset through the data
    for filename in os.listdir(directory):
        if filename.endswith('.JSF'):
            imgL = []
            imgR = []
            print("IMAGE LISTS RESET")
            


            # Prediction value is used to read the message length add 16 bits for the length
            # of the header then add it to the i value to skip over information we dont' need
            # without this we would need to parse through all of the information which drastically
            # increases run time
            prediction = 0

            # i is the value that I am using to iterate through the data and index values
            i = 0
            with open(os.path.join(directory, filename), 'rb') as f:
                data = f.read()

                # If the prediction leads to a value bigger than the length of the data
                # we won't be able to unpack the header struct so skip it.
                # The 16 represents the size of the header struct.
                while prediction <= len(data):
                    if prediction + 16 >= len(data):
                        break
                    f.seek(i)
                    header = f.read(header_struct.size)
                    marker, protocalVersion, sessionID, messageType, cmdType, subSysNum, channel, \
                    seqNum, reserved, msgSize = header_struct.unpack(header)

                    longitude = struct.unpack('<i', data[i+96:i+96+4])[0] / 10000 / 60
                    latitude =  struct.unpack('<i', data[i+100:i+100+4])[0] / 10000 / 60
                    # longitude, latitude = struct.unpack('<ii', data[i+96:i+96+8])[0]
                    # print(longitude)
                    # print(latitude)
                    currentLong = longitude
                    currentLat = latitude

                    if currentLong == prevLong and currentLat == prevLat:
                        same += 1
                        skip = True
                    else:
                        skip = False
                    prevLat = currentLat
                    prevLong = currentLong
                    # Checks for the beginning of the messages incase the prediction
                    # value lead us astray. Beginning of a message should
                    # always start with x1601 or decimal 5633
                    # Protocal version should also stay 14 for the
                    # time being so its there as another sanity check

                    if not skip:
                        if marker == 5633 and protocalVersion == 14:
                                
                                # Any message that shows a type larger than 2111 isn't included in the documentation
                                # and messes up the prediction so it is being ignored
                                if(messageType > 2112):
                                    pass
                                else:

                                    # Prediction size is calculated by taking the message size
                                    # and adding 16 to it for the size of the header then has
                                    # i added to it since i represents the current index
                                    # this allows us to skip directly to the header of the next
                                    # message 
                                    prediction = i + msgSize + 16

                                    # The message type that we are looking for is 80
                                    # this is the standard message that has a ton of
                                    # important information that we can use
                                    # subSysNum 20 represents the low frequency data
                                    # If there comes a time where we wish to also graph
                                    # high frequency data we can change the 20 to a 21
                                    if(messageType == 80) and subSysNum == 20:

                                        # account is being incremented to count the amount of
                                        # acoustic information we are parsing through
                                        account += 1

                                        # Channel 0 represents the port side of the vessel
                                        if channel == 0:

                                            # j is variable that we are using to index through
                                            # the echo intensity messages. We can get the size
                                            # of this by looking at the msgSize variable then adding
                                            # 240 for all of the information included in the
                                            # message type 80 message, then we add 16 for the size
                                            # of the header message
                                            j = i + 240 + 16
                                            echoIntensitiesL = []
                                            
                                            # j needs to stay less than or equal to the prediction because
                                            # if j gets larger than the prediction we will begin to look
                                            # at the next message
                                            while j <= prediction:
                                                try: 
                                                    # alpha = 7.5
                                                    val = struct.unpack('<h', data[j:j+2])[0]

                                                    val = val / 2
                                                    val = 40 * math.log10(val + 1) + alpha * val
                                                    # val = math.sqrt( (val / 2)**2)
                                                    j += 2
                                                    echoIntensitiesL.append(val)     
                                                except:
                                                    break

                                        # Channel 1 represents the starboard side of the vessel
                                        if channel == 1:
                                            j = i + 240 + 16
                                            # h = (struct.unpack('<i', data[i+136:i+136+4])[0])
                                            # depth = (struct.unpack('<i', data[i+136+16:i+16+136+4])[0]) * 10 **(-3)
                                            # validityFlag = (struct.unpack('<H', data[i+30+16:i+16+30+2])[0])
                                            h = (struct.unpack('<i', data[i+144+16:i+16+144+4])[0]) * 10 ** -3
                                            echoIntensitiesR = []
                                            while j <= prediction:
                                                try: 
                                                    val = struct.unpack('<h', data[j:j+2])[0]
                                                    val = val / 2
                                                    # alpha = 4
                                                    val = 40 * math.log10(val + 1) + alpha * val
                                                    # print(val)
                                                    # val = math.sqrt( (val / 2)**2 - (h)**2 )
                                                    # val = math.sqrt(((val / 2) ** 2) - ((h)**2))
                                                    # if (val/2) **2 > h**2:
                                                        # val = math.sqrt((val / 2) ** 2) - ((h)**2)
                                                    # val = math.sqrt( (val / 2)**2)
                                                    # if(val <= 0):
                                                        # print(f"val : {val}")

                                                    j += 2
                                                    echoIntensitiesR.append(val)
                                                except:
                                                    break
                                    # Set the index to the next prediction value so that
                                    # once we are done getting the echo intensity information
                                    # we can move onto the next message.
                                    i = prediction

                                    # Count is the variable used to show how many headers we are sorting through
                                    count += 1
                                    echoIntensitiesRev = list(reversed(echoIntensitiesR))
                                    # if len(echoIntensitiesL) != 0 and len(echoIntensitiesRev) != 0:
                                    # imgL.append(echoIntensitiesL)
                                    # imgR.append(echoIntensitiesRev)
                                    totalL.append(echoIntensitiesL)
                                    totalR.append(echoIntensitiesRev)
                            
                print(f"finished file : {filename}")
                finishedList.append(filename)
                print(f"Count : {count}")
                print(f"Msg 80 count: {account}")

                f.close()
                # splitup = filename.split(".")
                # filename = splitup[0] + ".png"
                # plt.savefig(filename)
            # Comment out to go through all files
            # break
    print(f"Length R:{len(totalR)}")
    print(f"Length L:{len(totalL)}")
    img = [[] for _ in range(len(totalL))]
    print(f"combined:{len(img)}")

    for i in range(len(totalL)):
        # img[i] = imgR[i] + imgL[i]
        img[i] = totalR[i] + totalL[i]
    # print(f"ImgR length:{len(imgR)}")
    # print(f"ImgL length:{len(imgL)}")
    # print(f"Total length:{len(imgR[1])}")
    print(same)
    setupGraph(img)
    plt.show()

main()