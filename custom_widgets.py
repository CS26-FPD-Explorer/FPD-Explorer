from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtCore
from numpy import arange, sin, pi
import numpy as np
import random
from PySide2.QtCore import Signal, Slot
from enum import Enum
import fpd
import fpd.fpd_processing as fpdp
import fpd.fpd_file as fpdf
from fpd.ransac_tools import ransac_1D_fit, ransac_im_fit
from ui_inputbox import Ui_InputBox
import fpd_processing_new as fpdp_new
from ui_loadingbox import Ui_LoadingBox
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        self.fig = Figure()
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
    def __init__(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x :str =None, text_y:str=None):
        """
        Create a new form with 2 input value x and Y and their output as power of 2         
        
        Parameters
        ----------
        initial_x : int
        default value for X
        initial_y : int
        default value for Y
        minimum : int
        minimum acceptable value
        maximum : int
        maximum acceptable value
        text_x : str
        text to show on the X form
        text_y : str
        text to show on the Y form
        """
        
        super(CustomInputForm,self).__init__()
        self.ui = Ui_InputBox()
        self.ui.setupUi(self)
        self.default_x = self.ui.Xsize.value()
        self.default_y = self.ui.Ysize.value()
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
        """
        Update the text box showing the 2^(input value) computed
        """
        self.ui.Xvalue.clear()
        self.ui.Yvalue.clear()

        self.ui.Xvalue.insert("= " + str(pow(2,self.ui.Xsize.value())))
        self.ui.Yvalue.insert("= " + str(pow(2,self.ui.Ysize.value())))

    @Slot()
    def restore_default(self):
        """
        Restore X and Y to their default value 
        """
        print("restoring to default")
        self.ui.Xsize.setValue(self.default_x)
        self.ui.Ysize.setValue(self.default_y)
        
    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Reset the value to its default to not mess up the loading
        """
        self.restore_default()
        return super().reject()

class Space_Buttons(Enum):
    REAL_SPACE = 0
    RECIP_SPACE = 1


class CustomLoadingForm(QtWidgets.QDialog):
    def __init__(self):
        """
        Set up a new loading form with 2 radio button and 2 progress bar
        """
        super(CustomLoadingForm, self).__init__()
        self.ui = Ui_LoadingBox()
        self.ui.setupUi(self)
        self.checked_value = Space_Buttons.REAL_SPACE
        self.sum_im = None
        self.ui.spaceGroup.setId(self.ui.realButton, 0)
        self.ui.spaceGroup.setId(self.ui.recipButton, 1)
        self.ui.realProgress.setValue(0)
        self.ui.recipProgress.setValue(0)
    
    def set_ds_sel(self, ds_sel):
        """
        Input the memory mapped MerlinBinary with skip
        
        Parameters
        ----------
        ds_sel : MerlinBinary Memory Map
        """
        self.ds_sel = ds_sel

    @Slot()
    def change_button(self):
        """
        Update the actual checked button
        """
        button = self.ui.spaceGroup.checkedId()
        self.checked_value = Space_Buttons(button).name  

    @Slot()
    def accept(self):
        """
        Overload of the accept function
        Update the progress bar with the loading of image based on which button has been clicked
        """
        if self.checked_value == Space_Buttons.REAL_SPACE:
            self.sum_im = fpdp_new.sum_im(
                self.ds_sel, 16, 16, widget = self.ui.realProgress)
        else:
            self.sum_im = fpdp_new.sum_dif(
                self.ds_sel, 16, 16, widget = self.ui.recipProgress)
        return super().accept()  

    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Make sure to use sum_im in case the user cancel
        and then close the widget
        """
        self.sum_im = fpdp_new.sum_im(self.ds_sel, 16, 16)
        return super().reject()
