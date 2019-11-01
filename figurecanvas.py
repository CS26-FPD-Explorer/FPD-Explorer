from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtCore
from numpy import arange, sin, pi
import numpy as np
import random

import fpd
import fpd.fpd_processing as fpdp
import fpd.fpd_file as fpdf
from fpd.ransac_tools import ransac_1D_fit, ransac_im_fit

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = self.fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def get_fig(self):
        return self.fig

    def get_axes(self):
        return self.axes

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        pass
        # x = np.linspace(0, np.pi*2, 50)
        # y = 2*x + 4

        # # add noise
        # y += (np.random.random(50)-1) * 0.5
        # # add outliers
        # bad_inds = np.arange(50) % 3.0 == 0
        # y[bad_inds] = np.random.random(bad_inds.sum()) + 1

        # # do regular fit
        # p = np.polyfit(x, y, 1)
        # yfit = np.polyval(p, x)

        # # plot
        # #self.axes.plot(x, y, label='Data')
        # #self.axes.plot(x, yfit, label='Fit')
        # fit, inliers, model = ransac_1D_fit(
        #     x, y, mode=1, residual_threshold=0.3)
        # outliers = inliers == False
        # self.axes.plot(x[inliers], y[inliers], 'bo', label='Inliers')
        # self.axes.plot(x[outliers], y[outliers], 'ro', label='Outliers')
        # self.axes.plot(x, fit, 'k-', label='Fit')
        # self.axes.legend(loc=0)



class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(1000)

    def compute_initial_figure(self):
        #self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        pass
    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


