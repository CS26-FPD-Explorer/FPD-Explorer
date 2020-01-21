import psutil
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

matplotlib.use('Qt5Agg')


class CpuFreqGraph(object):
    def __init__(self, ax):
        ##Needed to initialize the capture
        psutil.cpu_times_percent(interval=None)
        self.ax = ax
        self.x_data = np.arange(0, 100)
        self.user_data = np.zeros(100)
        self.system_data = np.zeros(100)
        self.ram_data = np.zeros(100)

        self.ax.set_xlim(0, 100)
        self.ax.set_ylabel("Usage (%)")
        self.ax.set_xlabel("Time")

        self.ax.set_ylim(0,100)


        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,
            labelbottom=False)      # ticks along the top edge are off
        self.ax.spines['right'].set_color(None)
        self.ax.spines['top'].set_color(None)


        self.cpu_percent = psutil.cpu_times_percent(interval=None)
        self.ram_percent = psutil.virtual_memory().percent

        self.user_data[0] = self.cpu_percent.user
        self.system_data[0] = self.cpu_percent.system
        self.ram_data[0] = self.ram_percent

        self.system_line, = self.ax.plot([], [], lw=2, label="System-CPU Usage", color='orange')
        self.system_line.set_data(self.x_data, self.system_data)

        self.user_line, = self.ax.plot([], [], label="User-CPU Usage", color=(17/256, 125/256, 187/256))
        self.user_line.set_data(self.x_data, self.user_data)

        self.ram_line, = self.ax.plot([], [], lw=2, label="Memory (RAM) Usage", color='purple')
        self.ram_line.set_data(self.x_data, self.ram_data)

        self.ax.legend(loc='upper left')


    def animate(self, i):

        self.user_data = np.roll(self.user_data,-1)
        self.system_data = np.roll(self.system_data,-1)
        self.ram_data = np.roll(self.ram_data, -1)

        self.cpu_percent = psutil.cpu_times_percent(interval=None)
        self.ram_percent = psutil.virtual_memory().percent

        self.user_data[-1] = self.cpu_percent.user
        self.system_data[-1] = self.cpu_percent.system
        self.ram_data[-1] = self.ram_percent

        self.user_line.set_data(self.x_data, self.user_data)
        self.system_line.set_data(self.x_data, self.system_data)
        self.ram_line.set_data(self.x_data, self.ram_data)

        return self.user_line, self.system_line,



def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls


fig, ax = plt.subplots()


cpu = CpuFreqGraph(ax)

ani = animation.FuncAnimation(
    fig, cpu.animate, interval=100, blit=False )
plt.show()

