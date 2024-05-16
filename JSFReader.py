import struct
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

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
    # message_type = b'\x80'
    # message_type = b'\x1601'
    message_type1 = b'\x01'
    message_type2 = b'\x16'


    directory = 'Immerse/SideScan 0/'
    for filename in os.listdir(directory):
        if filename.endswith('.JSF'):
            with open(os.path.join(directory, filename), 'rb') as f:
                header = f.read()
                for i in range(len(header)):
                    if header[i:i+1] == message_type2: # For 1601
                        if header[i:i+1] == message_type1:
                    # if header[i:i+1] == message_type:

                        # print(header[i:i+1])
                        # if i < 100000:
                            # print(header[i-10:i])
                            # print(header[i-10:i+5])
                            
                            print(header[i:i+20])
                            # marker = i
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


def old():
    counter = 0
    # Open the JSF file in binary mode
    with open('Immerse/SideScan 0/20240416-201317-UTC_0-2024-04-16_oahu_kohola_HFB5m_kuleana_spot_1-IVER3-3099_WP0.JSF', 'rb') as file:
        # Read the binary data
        binary_data = file.read()

        # Define the message type to search for (0x80 in hexadecimal)
        message_type = b'\x80'

        # Find all occurrences of the message type in the binary data
        message_indices = [i for i in range(len(binary_data)) if binary_data[i:i+1] == message_type]
        print("test")
        # Extract data for each message of type 0x80
        for index in message_indices:
            # Assuming the data follows the message type and has a fixed length of 4 bytes
            data_start_index = index + 0
            data_end_index = data_start_index + 0
            message_data = binary_data[data_start_index:data_end_index]

            # Process the extracted data (e.g., convert bytes to integer)
            # You may need to adjust the data processing based on the actual format of the data
            data_value = int.from_bytes(message_data, byteorder='big')  # Convert bytes to integer
            print(f"Data for message type 0x80: {hex(data_value)}")
            counter +=1
            print(counter)


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