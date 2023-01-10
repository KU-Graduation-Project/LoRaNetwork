import matplotlib.animation as animation
import matplotlib.pyplot as plt

class drawGraph :
    def __init__(self):
        return

    def __init_func(self, line):
        line.set_data([], [])
        return line,

    # animation function
    def __animate(self, i, data, xdata, ydata, axis, line, x_width):
        # with the frame number

        # x, y values to be plotted
        x = i
        y = 0

        if data.empty() == False:
            data.task_done()
            y = data.get()

        # appending values to the previously
        # empty x and y data holders
        xdata.append(x)
        ydata.append(y)
        axis.set_xlim(max(xdata)-x_width, max(xdata))
        line.set_data(xdata, ydata)

        return line,

    #main Function : draw graph
    #Parmater : data, period(주기),
    #           start(data array에서 그리기 시작하는 위치),
    #           x_width(보여지는 총 x넓이),
    #           y_min(y의 최소값),
    #           y_max(y의 최대값)... 추가 예정
    def drawgraph(self, data, start, period, x_width, y_min, y_max) :
        fig = plt.figure()
        axis = plt.axes(xlim=(start, x_width+start),
                        ylim=(y_min, y_max))

        #Change to milliseconds
        period = period*1000

        #lw차이 점검 하기
        line, = axis.plot([], [], lw=2)
        line.set_data([], [])
        xdata = []
        ydata = []

        anim = animation.FuncAnimation(fig, self.__animate,
                                       fargs= (data, xdata, ydata, axis, line, x_width, ),
                                       frames=500,
                                       interval=period,
                                       blit=True)

        plt.show()
        return;
