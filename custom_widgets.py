from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QRunnable, QThreadPool, QObject
from numpy import arange, sin, pi
import numpy as np
import random
from PySide2.QtCore import Signal, Slot
from enum import Enum
import fpd
from ui_loadingbox import Ui_LoadingBox
import fpd.fpd_processing as fpdp
import fpd.fpd_file as fpdf
from fpd.ransac_tools import ransac_1D_fit, ransac_im_fit
from ui_inputbox import Ui_InputBox
import fpd_processing_new as fpdp_new
from PySide2.QtWidgets import QProgressBar


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
        Reset the value to its default to not mess up the loading"""
        self.restore_default()
        return super().reject()

class CustomLoadingForm(QtWidgets.QDialog):
    def __init__(self, ds_sel):
        """
        Set up a new loading form with 2 progress bar
        Parameters
        ----------
        ds_sel : MerlinBinary Memory Map

        """
        super(CustomLoadingForm, self).__init__()
        self.ui = Ui_LoadingBox()
        self.ui.setupUi(self)
        self.ds_sel = ds_sel
        self.sum_im = None
        self.sum_diff = None
        #set min and max value (Based on their code)
        self.ui.realProgress.setValue(0)
        self.ui.realProgress.setMinimum(0)
        self.ui.realProgress.setMaximum(np.prod(self.ds_sel.shape[:-2]))
        print(np.prod(self.ds_sel.shape[:-2]))
        self.ui.recipProgress.setValue(0)
        self.ui.recipProgress.setMinimum(0)
        self.ui.recipProgress.setMaximum(np.prod(self.ds_sel.shape[:-2]))
        
        #create 2 thread and assign them signals based on the custum signals classes
        # First paramenter is the return value and second the fnct to call
        # Other are argument to pass to the function
        self.nb_thread = 2
        self.threadpool = QThreadPool()
        worker = GuiUpdater(self.sum_im, fpdp_new.sum_im, self.ds_sel, 16, 16)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)


        worker2 = GuiUpdater(self.sum_diff, fpdp_new.sum_dif, self.ds_sel, 16,
                               16)
        worker2.signals.finished.connect(self.thread_complete)
        worker2.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker2)
    
    @Slot(tuple)
    def progress_fn(self,value):
        print(value)
        if value[1] == "sum_diff":
            self.ui.recipProgress.setValue(self.ui.recipProgress.value()+value[0])
        else:
            self.ui.realProgress.setValue(
                self.ui.realProgress.value()+value[0])

    @Slot()
    def thread_complete(self):
        self.nb_thread-=1
        if self.nb_thread == 0: #Make sure both thread are done
            return super().done(True)

class CustomSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `tuple` (int : indicating % progress, caller) 

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(tuple)

class GuiUpdater(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, return_value, fn, *args, **kwargs):
        super(GuiUpdater, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = CustomSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress


    @Slot()  # QtCore.Slot
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            return_value = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()  # Done
