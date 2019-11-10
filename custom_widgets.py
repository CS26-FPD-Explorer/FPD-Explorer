from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtCore
from numpy import arange, sin, pi
import numpy as np
import random
from PySide2.QtCore import Signal, Slot

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
        self.default_x = self.ui.Xsize.value()
        self.default_y = self.ui.Ysize.value()

    def update_form(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
        self.ui.Xsize.setRange(minimum, maximum)
        self.ui.Ysize.setRange(minimum, maximum)
        self.ui.Xsize.setValue(initial_x)
        self.ui.Ysize.setValue(initial_y)
        self.default_x = initial_x
        self.default_y = initial_y

        if text_x:
            self.ui.Xtext.clear()
            self.ui.Xtext.insert(text_x)
        if text_y:
            self.ui.Ytext.clear()
            self.ui.Ytext.insert(text_y)

    @Slot(int)
    def update_value(self):
        self.ui.Xvalue.clear()
        self.ui.Yvalue.clear()

        self.ui.Xvalue.insert("= " + str(pow(2,self.ui.Xsize.value())))
        self.ui.Yvalue.insert("= " + str(pow(2,self.ui.Ysize.value())))

    @Slot()
    def restore_default(self):
        self.ui.Xsize.setValue(self.default_x)
        self.ui.Ysize.setValue(self.default_y)

    @Slot()
    def reject(self):
        self.restore_default()
        return super().reject()

