import struct
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

# All data included in the header. Channel says if data is port or starboard, 0 port, 1 starboard
marker = protocalVersion = sessionID = messageType = cmdType = subSysNum = channel = seqNum = reserved = msgSize = b'\x00'
# 0-1          2               3           4-5          6          7          8         9       10-11      12-15    

x_coords = []
y_coords = []
z_coords = []
# define the header structure
# OLD STRUCT SIZE, NOT CORRECT
# header_struct = struct.Struct('<5siiiiiiffii')
header_struct = struct.Struct('<hbbhbbbbhl')

# define the ping structure
ping_struct = struct.Struct('<IIfiiiihhhhhhhhhh')
def current():
    counter = 0
    marker = b'\x1601'
    msgType = hex(128)
    marker = b'\x80'

# header_struct.unpack(header)
    directory = 'Immerse/Sidescans/SideScan 0/'
    for filename in os.listdir(directory):
        if filename.endswith('.JSF'):
            with open(os.path.join(directory, filename), 'rb') as f:
                header = f.read()
                for i in range(len(header)):
                    if header[i:i+3] == marker: # For 1601
                        # print(header[i:i+2])
                        print(header[i:i+15])
                        # if msgType in header[i:i+10]:
                        if b'\x80' in header[i:i+10]:
                            print("WORKED")
                            print(header[i:i+10])
                            counter +=1
                print(counter)

    # with open('Immerse/SideScan 0/20240416-201317-UTC_0-2024-04-16_oahu_kohola_HFB5m_kuleana_spot_1-IVER3-3099_WP9.JSF', 'rb') as f:
        # header = f.read()
        # for i in range(len(header)):
        #     if header[i:i+3] == message_type: # For 1601
        #     # if header[i:i+1] == message_type:

        #         # print(header[i:i+1])
        #         # if i < 100000:
        #             # print(header[i-10:i])
        #             # print(header[i-10:i+5])
                    
        #         print(header[i:i+20])
        #         # marker = i
        #         counter +=1
        # print(counter)
        # marker, B2, B3, messageType, B6, B7, B8, B9, reserved, messageSize = header_struct.unpack(header)
        # print(hex(marker))
        # print(hex(messageType))

        # OLD CODE
        # magic_number, file_format_version, file_size, ping_count, first_ping_offset, \
        # last_ping_size, sample_format, sample_rate, sonar_id, ping_period, \
        # range_scale_factor = header_struct.unpack(header)

        # read the pings
        # print(ping_count)
        # for i in range(ping_count):
        #     # go to the offset of the current ping
        #     f.seek(first_ping_offset + i * ping_struct.size)
            
        #     # read the ping
        #     ping = f.read(ping_struct.size)
        #     ping_number, ping_seconds, ping_microseconds, sonar_x, sonar_y, \
        #     sonar_depth, ping_flags, speed_of_sound, beam_count, \
        #     samples_per_beam, bytes_per_sample, data_type, ping_quality, \
        #     detection_info, reserved1, reserved2, reserved3 = ping_struct.unpack(ping)
        #     print(i)
            # process the ping data
            # ...
            # TODO
            # Once order of data is figured out need to figure out how to graph the data in 2D first then in 3D
            
            # print(f"{sonar_x}, {sonar_y}, {sonar_depth} \n\n")
            # if sonar_x == 0:
            #     theta = math.atan(0)
            # else:
            #     theta = math.atan(sonar_y / sonar_x)
            # r = math.sqrt(sonar_x ** 2 * sonar_y **2)
            # x_coords.append(r)
            # y_coords.append(theta)


    # # # Creating data
    # # # x = np.linspace(-5, 5, 100)
    # # # y = np.linspace(-5, 5, 100)
    # # X, Y = np.meshgrid(x_coords, y_coords)
    # # # 
    # # Z = np.sin(X) + np.cos(Y)
    # # # Z = z_coords

    # # # Creating a 3D plot
    # # fig = plt.figure()
    # # ax = fig.add_subplot(111, projection='3d')

    # # # Plotting the 3D contour
    # # ax.contour3D(X, Y, Z, 50, cmap='viridis')

    # # # Customizing the plot
    # # ax.set_xlabel('X-axis')
    # # ax.set_ylabel('Y-axis')
    # # ax.set_zlabel('Z-axis')
    # # ax.set_title('Basic 3D Contour Plot')

    # # # Displaying the plot
    # # plt.show()


def main():
    current()

main()



# case 80:
# 	  Sonar++;
# 	  break;
# 	case 82:
# 	  Sidescan++;
# 	  break;
# 	case 2020:
# 	  Pitch++;
# 	  break;
# 	case 2002:
# 	  NMEA++;
# 	  break;
# 	case 2060:
# 	  Press++;
# 	  break;
# 	case 2040:
# 	  Analog++;
# 	  break;
# 	case 2080:
# 	  Doppler++;
# 	  break;
# 	case 2091:
# 	  Situation++;
# 	  break;
# 	case 86:
# 	  SAS++;
# 	  break;
# 	case 182:
# 	  S_info++;
# 	  break;
# 	case 2100:
# 	  Cable++;
# 	  break;
# 	case 9002:
# 	  SitII++;
# 0 – 1
# Marker for the Sync/Start of Header (always 0x1601)
# This serves as a sanity check during file processing.
# UINT16
# 2
# Protocol Version (e.g. 0xD).
# The protocol level indicates which revision of this specification was
# used to write that message. Messages of differing protocol levels
# may be interspersed in the same file. Protocol-level changes may
# involve additional messages or changes to the non-public portion of
# the interface.
# UINT8
# 3
# Session Identifier
# The session identifier is used for internal routing and can be ignored.
# UINT8
# 4 – 5
# Message Type (e.g. 80 = Acoustic Return Data)
# This field defines the type of data to follow. Some data formats of
# interest are detailed in the following sections. If this field contains
# an unwanted or unknown (i.e., not defined) type, use the Size of the
# Message (bytes 12– 15) to skip over the data to the next message
# header. The message protocol is used for command and control and
# data.
# UINT16
# 6
# Command Type
# 2 = Normal data source
# The command type field can typically be ignored when reading JSF
# files as this parameter may only be of interest during real-time
# operation.
# UINT8
# 7
# Subsystem Number
# The subsystem number determines the source of data; common
# subsystem assignments are:
# Sub-Bottom (SB) = 0
# Low frequency data of a dual-frequency side scan = 20
# High frequency data of a dual-frequency side scan = 21
# Very High frequency data of a tri-frequency side scan = 22
# UINT8
# 3
# BYTE OFFSETS DESCRIPTION SIZE
# Bathymetric low frequency data of a dual side scan=40
# Bathymetric high frequency data of a dual side scan=41
# Bathymetric very high frequency of a tri-frequency=42
# Bathymetric motion tolerant, low frequency dual side scan=70
# Bathymetric motion tolerant high frequency dual side scan=71
# Bathymetric motion tolerant very high frequency tri-frequency=72
# Raw Serial/UDP/TCP data =100
# Parsed Serial/UDP/TCP data =101
# Gap Filler data =120
# Standard side scan systems are single or dual frequency. When more
# than two side scan frequencies are present, the subsystem number
# begins at 20 and increases with increasing acoustic center
# frequencies.
# 8
# Channel for a Multi-Channel Subsystem
# For Side Scan Subsystems:
# 0 = Port
# 1 = Starboard
# For Serial Ports: this will be the logical port number, which often
# differs from the physical COM port in use.
# The single-channel sub-bottom systems channel is 0.
# UINT8
# 9 Sequence Number UINT8
# 10 – 11 Reserved UINT16
# 12 – 15
# Size of the following message in bytes
# The byte count is the number of bytes until the start of the next
# message header. This is the amount of additional data to read if
# processing the current message or the am