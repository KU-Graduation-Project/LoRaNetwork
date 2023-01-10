#data 가지고 그래프 그리기
#data가 다른 Thread로 계속 업데이드, 계속 그래프 그리기
#입력이 찍혔으면 좋겠는거
from typing import List

import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
import threading

fig = plt.figure()
ax = plt.axes(xlim = (0,4), ylim = (-2,2))
line, = ax.plot([], [], lw = 3)
data =  [0.5, 1.2, 2, 3]
def animate(data) :
    # print(round(i))
    # x = data[0]
    x = np.linspace(data[0], data[1], 40)
    y = x*0.5
    line.set_data(x, y)
    return line,

def inputF(data) :
    while True :
        input_data = input("<<")
        i = 0
        if  type(input_data) != 'int' :
            break
        else :
            data[i] = input_data
    return data

# data = threading.Thread(target = "inputF", args=(data)).start()
anim = FuncAnimation(fig, animate, frames=data, interval=200)

plt.show()


