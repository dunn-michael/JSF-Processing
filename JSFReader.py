import struct
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

x_coords = []
y_coords = []
z_coords = []
# define the header structure
# OLD STRUCT SIZE, NOT CORRECT
# header_struct = struct.Struct('<5siiiiiiffii')
header_struct = struct.Struct('<hbbhbbbbhl')

# define the ping structure
ping_struct = struct.Struct('<IIfiiiihhhhhhhhhh')

# open the file in binary mode
with open('Immerse/SideScan 0/20240416-201317-UTC_0-2024-04-16_oahu_kohola_HFB5m_kuleana_spot_1-IVER3-3099_WP9.JSF', 'rb') as f:
    # read the header
    header = f.read(header_struct.size)
    marker, B2, B3, messageType, B6, B7, B8, B9, reserved, messageSize = header_struct.unpack(header)
    print(hex(marker))
    print(hex(messageType))

    # OLD CODE
    # magic_number, file_format_version, file_size, ping_count, first_ping_offset, \
    # last_ping_size, sample_format, sample_rate, sonar_id, ping_period, \
    # range_scale_factor = header_struct.unpack(header)

    # read the pings
    # print(ping_count)
    for i in range(ping_count):
        # go to the offset of the current ping
        # f.seek(first_ping_offset + i * ping_struct.size)

        # read the ping
        ping = f.read(ping_struct.size)
        ping_number, ping_seconds, ping_microseconds, sonar_x, sonar_y, \
        sonar_depth, ping_flags, speed_of_sound, beam_count, \
        samples_per_beam, bytes_per_sample, data_type, ping_quality, \
        detection_info, reserved1, reserved2, reserved3 = ping_struct.unpack(ping)
        print(i)
        # process the ping data
        # ...
        # print(f"{sonar_x}, {sonar_y}, {sonar_depth} \n\n")
        if sonar_x == 0:
            theta = math.atan(0)
        else:
            theta = math.atan(sonar_y / sonar_x)
        r = math.sqrt(sonar_x ** 2 * sonar_y **2)
        x_coords.append(r)
        y_coords.append(theta)


# # Creating data
# # x = np.linspace(-5, 5, 100)
# # y = np.linspace(-5, 5, 100)
# X, Y = np.meshgrid(x_coords, y_coords)
# # 
# Z = np.sin(X) + np.cos(Y)
# # Z = z_coords

# # Creating a 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plotting the 3D contour
# ax.contour3D(X, Y, Z, 50, cmap='viridis')

# # Customizing the plot
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')
# ax.set_title('Basic 3D Contour Plot')

# # Displaying the plot
# plt.show()