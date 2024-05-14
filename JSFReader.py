import struct
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

x_coords = []
y_coords = []
z_coords = []

# define the header structure
header_struct = struct.Struct('>5siiiiiiffii')

# define the ping structure
ping_struct = struct.Struct('>IIfiiiihhhhhhhhhh')

# open the file in binary mode
with open('Immerse/dataSet.JSF', 'rb') as f:
    # read the header
    header = f.read(header_struct.size)
    magic_number, file_format_version, file_size, ping_count, first_ping_offset, \
    last_ping_size, sample_format, sample_rate, sonar_id, ping_period, \
    range_scale_factor = header_struct.unpack(header)

    # read the pings
    for i in range(ping_count):
        # go to the offset of the current ping
        # f.seek(first_ping_offset + i * ping_struct.size)

        # read the ping
        ping = f.read(ping_struct.size)
        ping_number, ping_seconds, ping_microseconds, sonar_x, sonar_y, \
        sonar_depth, ping_flags, speed_of_sound, beam_count, \
        samples_per_beam, bytes_per_sample, data_type, ping_quality, \
        detection_info, reserved1, reserved2, reserved3 = ping_struct.unpack(ping)

        # process the ping data
        # ...
        print(f"{sonar_x}, {sonar_y}, {sonar_depth} \n\n")
        x_coords.append(sonar_x)
        y_coords.append(sonar_y)
        z_coords.append(sonar_depth)


# Creating data
# x = np.linspace(-5, 5, 100)
# y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_coords, y_coords)
# 
# Z = np.sin(X) + np.cos(Y)
Z = z_coords

# Creating a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting the 3D contour
ax.contour3D(X, Y, Z, 50, cmap='viridis')

# Customizing the plot
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('Basic 3D Contour Plot')

# Displaying the plot
plt.show()