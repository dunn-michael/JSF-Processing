import os
from struct import *
import struct

# Read in the file
# file_data = ...
# Loop through parsing one message at a time
# val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13 = 0
header_struct = struct.Struct('<HBBHBBBBHi')
prediction = 0
fail = False
i = 0
count = 0
with open("JSF-Processing/Sidescans/20240416-201317-UTC_0-2024-04-16_oahu_kohola_HFB5m_kuleana_spot_1-IVER3-3099_WP14.JSF", 'rb') as f:
    data = f.read()
    while i != len(data):
    # for i in range(len(data)):
        # print(i)
        f.seek(i)
        header = f.read(header_struct.size)
        marker, protocalVersion, sessionID, messageType, cmdType, subSysNum, channel, \
        seqNum, reserved, msgSize = header_struct.unpack(header)
        if marker == 5633:
            if protocalVersion == 14:
                if(messageType > 2112):
                    pass
                else:
                    if prediction != i:
                        print("--------=WRONG CALCULATION=--------")
                        fail = True
                    # if data[i+4] + data[i+5] == 80:
                    print(messageType)
                    # prediction = i + msgSize + 16
                    prediction = i + msgSize + 16
                    print(f"current i:{i}")
                    print(f"after adding:{prediction}\n")
                    i = prediction
                    print(f"Added:{i}")
                    count +=1
                    if fail:
                        break
                    # print({data[i + 6]})
                    # if i >= 100000:
                    #     break

    print(f"Total Count : {count}")



    # # read = file_data.read(header_struct.size)
    # # data = file_data.read()
    
    # # Get message type and size
    # # message_type = msg_header[0]
    # # message_size = msg_header[9]

    # # Isolate the message data and remove it from the file data variable
    # message_data = file_data.seek(message_size)
    # print(message_data)
    # # file_data = file_data[message_size:]
    # # Only process message 80
    # if message_type == 80:
    #     print("WORKED")
    #     # Remove the first 16 bits because we already processed those
    #     message_data = message_data[16:]
    #     # Split into header and sensor data
    #     # header_info = struct.unpack('<[stuff]', message_data[:240])
    #     message_data = message_data[240:]
    #     # Read the raw acoustic data into a list
    #     acoustic_data = []
    #     num_bits = len(message_data)
    #     start_idx = 0
    #     stop_idx = [16]
    #     while stop_idx <= num_bits:
    #         # val = struct.unpack('<[thing]', message_data[start_idx:stop_idx])
    #         # acoustic_data.append(val)
    #         start_idx += 2
    #         stop_idx += 2
f.close()