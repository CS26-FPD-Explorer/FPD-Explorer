# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

import numpy as np
import psutil
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CpuFreqGraph(FigureCanvas, FuncAnimation):
    def __init__(self, parent=None):
        self._fig = Figure()
        ax = self._fig.add_subplot(111)
        FigureCanvas.__init__(self, self._fig)
        FuncAnimation.__init__(self, self._fig, self.animate, interval=100, blit=False)
        self.setParent(parent)

        # Needed to initialize the capture
        psutil.cpu_times_percent(interval=None)
        self.ax = ax
        self.x_data = np.arange(0, 100)
        self.user_data = np.zeros(100)
        self.system_data = np.zeros(100)
        self.ram_data = np.zeros(100)

        self.ax.set_xlim(0, 100)
        self.ax.set_ylabel("Usage (%)")
        self.ax.set_xlabel("Time")

        self.ax.set_ylim(0, 100)
        self.ax.get_xaxis().set_ticks([])
        self.ax.spines['right'].set_color(None)
        self.ax.spines['top'].set_color(None)

        self.cpu_percent = psutil.cpu_times_percent(interval=None)
        self.ram_percent = psutil.virtual_memory().percent

        self.user_data[0] = self.cpu_percent.user
        self.system_data[0] = self.cpu_percent.system
        self.ram_data[0] = self.ram_percent

        self.system_line, = self.ax.plot([], [], lw=2, label="System-CPU Usage", color='orange')
        self.system_line.set_data(self.x_data, self.system_data)

        self.user_line, = self.ax.plot([], [], label="User-CPU Usage", color=(17 / 256, 125 / 256, 187 / 256))
        self.user_line.set_data(self.x_data, self.user_data)

        self.ram_line, = self.ax.plot([], [], lw=2, label="Memory (RAM) Usage", color='purple')
        self.ram_line.set_data(self.x_data, self.ram_data)

        self.ax.legend(loc='upper left')

    def animate(self, i):

        self.user_data = np.roll(self.user_data, -1)
        self.system_data = np.roll(self.system_data, -1)
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
