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
from ui_inputbox import Ui_InputBox

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = self.fig.add_subplot(111)

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


class CustomInputForm(QtWidgets.QDialog):
    def __init__(self):
        super(CustomInputForm,self).__init__()
        self.ui = Ui_InputBox()
        self.ui.setupUi(self)
