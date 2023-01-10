from matplotlib import pyplot as plt
from matplotlib import animation
import serial
import numpy as np

fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(0, 30))
line, = ax.plot([], [], lw=2)

max_points = 11
line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float)*np.nan, lw=2)

ser = serial.Serial('COM4', 9600, timeout=1)

def init():
    if ser.readable() :
        return line,
    else :
        return 0
    return 0

def animate(i):
    print(i)
    y = ser.readline().decode()
    y = float(y)

    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    return line,


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=False)

plt.show()