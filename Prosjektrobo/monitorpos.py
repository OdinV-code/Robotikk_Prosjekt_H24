import socket
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# Set up UDP server to receive data from Tello
host = ''
port = 8890  # Tello's status port
locaddr = (host, port)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(locaddr)

# Set up the 3D plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_zlabel("Z (cm)")
ax.set_title("Drone Position (X, Y, Z)")

# Initialize lists to store coordinates
x_data, y_data, z_data = [], [], []

print("Monitoring Tello's Position...")

try:
    while True:
        # Receive data from Tello
        data, _ = sock.recvfrom(1024)
        data = data.decode('utf-8')

        # Parse the data string to extract x, y, z values
        status_dict = dict(item.split(":") for item in data.split(";") if ":" in item)
        x = int(status_dict.get('x', -1))  # -1 if x is not available
        y = int(status_dict.get('y', -1))  # -1 if y is not available
        z = int(status_dict.get('z', -1))  # -1 if z is not available

        # Print the positions in the terminal
        print(f"{time.strftime('%H:%M:%S')} - X: {x} cm, Y: {y} cm, Z: {z} cm")

        # Update the plot with the new data
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)
        ax.clear()
        ax.plot(x_data, y_data, z_data, marker='o')
        ax.set_xlabel("X (cm)")
        ax.set_ylabel("Y (cm)")
        ax.set_zlabel("Z (cm)")
        ax.set_title("Drone Position (X, Y, Z)")
        plt.pause(0.1)  # Update plot

except KeyboardInterrupt:
    print("Stopping monitoring...")

finally:
    sock.close()
    plt.ioff()
    plt.show()
