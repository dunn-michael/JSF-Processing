import struct
import os



# %matplotlib inline
import matplotlib.pyplot as plt
# plt.style.use('seaborn-white')
import numpy as np



# define the header structure
# header_struct = struct.Struct('<HBBHBBBBHi')


# define the ping structure
# ping_struct = struct.Struct('<IIfiiiihhhhhhhhh')

# This is the data struct that shows almost every variable we will need. For this to work you will need to add the
# corresponding missing variables down below where the struct is being unpacked
# data_struct = struct.Struct('lLLhhHHHhhhhHHhhhhhffhhhhhhhhhhhhfllhBBBBBBBBBBBBBBBBBBBBBBBBHLHhhHHHllHHlffhhhhhh')

# This includes both the header and the data
data_struct = struct.Struct('HBBHBBBBHiiIIhhHHHhhhhHHhhhhhffhhhhhhhhhhhhfiih\
                            BBBBBBBBBBBBBBBBBBBBBBBBHIHhhHHHiiHHiffhhhhhhhhHhh')
#  B = uint8 H = uint16 I = uint32 f = float
#  b = int8 h = int16 i = int 32 f = float


def graph():
    pass




def main():
    binCounter = 0
    binList = []
    x = []
    y = []
    z = []
    output = ''
    while(output != 'Y' and output != 'N'):
        output = str(input("Would you like to print the outputs? (Y/N) : ")).upper()
    # Goes through your directory to find files
    # directory = 'Sidescans/'
    directory = 'JSF-Processing/Sidescans/'
    for filename in os.listdir(directory):
        if filename.endswith('.JSF'):
            with open(os.path.join(directory, filename), 'rb') as f:
                sensorCount = 0
                # read the header
                test = f.read()
                for i in range(len(test)):

                    # This is here for testing to speed up tests
                    # f.seek(0 + i * data_struct.size)

                    # This will be the normal one
                    f.seek(i)
                    
                    # This takes the data from the file and only gathers the amount that it will to fill the variables
                    if i < 164051000:
                    # if i < 64051000:
                    # if i < 14051000:
                        header = f.read(data_struct.size)
                        # header = f.read(NMEA_struct.size)

                        # Takes the data out and assigns it to each variable. This corresponds to the
                        # sizes shown in the data_struct variable.
                        marker, protocalVersion, sessionID, messageType, cmdType, subSysNum, channel, \
                        seqNum, reserved, msgSize, time, startingDepth, pingNumber,reserved1, reserved2, \
                        MSB, LSB, LSB2, reserved3, reserved4, reserved5, ID, validityFlag, reserved6, dataFormat, \
                        distanceToTow1, distanceToTow2, reserved7, reserved8, kmOfPipe, heave, reserved9, \
                        reserved10, reserved11, reserved12, reserved13, reserved14, reserved15, reserved16, \
                        reserved17, reserved18, reserved19, reserved20, gapFiller, longitude, latitude, coordUnits,\
                        annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, \
                        annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, \
                        annotStr, annotStr, annotStr, annotStr, annotStr, annotStr, samples, sampInterv, gainFact,\
                        transmitLevel, reserved21, startTransmitPulFreq, endTransmitPulFreq, sweepLen, press, depthMM, sampleFreq,\
                        outgoingPulseID, AltitudeMM, soundSpeedMpS, mixerFreq, year, day, hour, minute, second, timeBasis,\
                        weightFactor, numberOfPulses, compassHeading, pitch, roll= data_struct.unpack(header)

                        # Every set of data should start with decimal 5633 (0x1601 hex)
                        if(marker == 5633):

                            # Message type 80 shows data collection
                            if messageType == 80:
                                if coordUnits == 1 or coordUnits == 2 or coordUnits == 3 or coordUnits == 4:
                                    # pass
                                    if ID == 1:
                                        # longitude = round(((longitude / 10000) / 60),3)
                                        longitude = (longitude / 10000) / 60
                                        latitude = (latitude / 10000) / 60
                                        if(channel == 1):
                                            side = "Starboard / Right"
                                            if subSysNum == 20:
                                                binCounter += 1
                                                binList.append(binCounter)
                                            #     x.append()
                                            #     y.append()
                                            #     z.append()
                                        elif channel == 0:
                                            side = "Port / Left"
                                        else:
                                            side = "INVALID"
                                        # This is just here for testing so I can see the values. Later this will be a graph
                                        if(output == 'Y'):
                                            # print(f"\n\nMarker:{hex(marker)} MSGTYPE:{messageType} Channel:{channel} Side:{side}")
                                            # print(f"Longitude:{longitude} Latitude:{latitude} coordUnit:{coordUnits} ID:{ID} Depth:{depthMM}")
                                            # print(f"Validity Flag:{bin(validityFlag)} Sub System Num:{subSysNum} Time:{time} Message Length:{msgSize}")
                                            # print(f"Number of Pulses:{numberOfPulses} Weighting Factor:{weightFactor}")
                                            # print(f"Pitch:{(pitch * 2**(-weightFactor))}")
                                            # print(f"Roll:{(roll * 2**(-weightFactor))}")
                                            # print(f"Compass:{(compassHeading * 2**(-weightFactor))}")
                                            # print(f"Protocal Version:{protocalVersion}")
                                            print(f"marker:{marker}, protocalVersion:{protocalVersion}, sessionID:{sessionID}, messageType:{messageType}, cmdType:{cmdType}, subSysNum:{subSysNum}, channel:{channel}, seqNum:{seqNum}, reserved:{reserved}, msgSize:{msgSize}")
                                            print(f"Data Format:{dataFormat}")
                                        sensorCount += 1
                    else:
                        print(f"Total Sensor Measurements : {sensorCount}")
                        # graph(x,y,z)
                        break
    f.close()

main()


# TODO
# Write code that checks the size of the file and stops unpacking data before it crashes
# and exits the for loop so it can move onto the next file

# Convert longitude and latitude frm 10000 * Minutes of arc to mmm?

# Make the countour plot 3D

# Compare the plots to the processed data to ensure accuracy

# Export the processed images as their own files that can be shared or used for other programs

# Add Error Checking?

# Add function that opens up file explorer so you choose the folder to go through instead of being predeclared


