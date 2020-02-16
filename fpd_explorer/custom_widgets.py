import numpy as np
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QObject, QRunnable, QThreadPool
from matplotlib.figure import Figure
from PySide2.QtWidgets import QDockWidget, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# FPD Explorer
from .custom_fpd_lib import fpd_processing as fpdp_new
from .res.ui_inputbox import Ui_InputBox
from .res.ui_loadingbox import Ui_LoadingBox
from .res.ui_inputBoxCenterOfMass import Ui_CenterofMass
from .res.ui_inputBoxCircularCenter import Ui_CircularCenterInput
from .res.ui_inputBoxRemoveAperture import Ui_RemoveAperture
from .res.ui_loadingboxCenterOfMass import Ui_LoadingBoxCenterOfMass


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        self._fig = Figure()

        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def get_fig(self):
        return self._fig

    def get_canvas(self):
        return self


class Pop_Up_Widget(QtWidgets.QWidget):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """

    def __init__(self, ApplicationWindow, tab_name=""):
        super(Pop_Up_Widget, self).__init__()
        self.application_window = ApplicationWindow
        self.tab_name = tab_name
        self.main_window = QMainWindow()
        self.main_widget = QtWidgets.QWidget()
        # self.main_window.setCentralWidget(self.main_widget)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(lambda: self.close_handler())
        buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setDefault(True)

        self.gridLayout = QVBoxLayout()
        self.gridLayout.addWidget(self.main_window)
        self.gridLayout.addWidget(buttonBox)
        self.main_widget.setLayout(self.gridLayout)

        self._docked_widgets = []
        # self.application_window._ui.tabWidget.tabCloseRequested.connect(self.close_handler)

    def setup_docking(self, name, location="Top"):
        """
        Initialize a dock widget with the given name
        Parameters
        ----------
        name : str the name of the dock widget window

        Return
        ---------
        widget : QWidget the widget inside of the dock widget
        """
        widget = MyMplCanvas(self)

        dock = QDockWidget(self)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea |
                             Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        if location == "Bottom":
            loc = Qt.BottomDockWidgetArea
        elif location == "Left":
            loc = Qt.LeftDockWidgetArea
        elif location == "Right":
            loc = Qt.RightDockWidgetArea
        else:
            loc = Qt.TopDockWidgetArea
        self.main_window.addDockWidget(loc, dock)
        self._docked_widgets.append(dock)
        self.tab_index = self.application_window._ui.tabWidget.addTab(self.main_widget, self.tab_name)
        self.application_window._ui.tabWidget.setCurrentIndex(self.tab_index)

        return widget

    def close_handler(self):
        self.application_window._ui.tabWidget.removeTab(self.tab_index)
        for el in self._docked_widgets:
            el.close()
            del el


class CustomInputForm(QtWidgets.QDialog):
    def __init__(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x: str = None, text_y: str = None):
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

        super(CustomInputForm, self).__init__()
        self._ui = Ui_InputBox()
        self._ui.setupUi(self)
        self._default_x = self._ui.Xsize.value()
        self._default_y = self._ui.Ysize.value()
        self._ui.Xsize.setRange(minimum, maximum)
        self._ui.Ysize.setRange(minimum, maximum)
        self._ui.Xsize.setValue(initial_x)
        self._ui.Ysize.setValue(initial_y)
        self._default_x = initial_x
        self._default_y = initial_y

        if text_x:
            self._ui.Xtext.clear()
            self._ui.Xtext.insert(text_x)
        if text_y:
            self._ui.Ytext.clear()
            self._ui.Ytext.insert(text_y)

    @Slot(int)
    def update_value(self):
        """
        Update the text box showing the 2^(input value) computed
        """
        self._ui.Xvalue.clear()
        self._ui.Yvalue.clear()
        self._ui.Xvalue.insert("= " + str(pow(2, self._ui.Xsize.value())))
        self._ui.Yvalue.insert("= " + str(pow(2, self._ui.Ysize.value())))

    @Slot()
    def restore_default(self):
        """
        Restore X and Y to their default value
        """
        print("restoring to default")
        self._ui.Xsize.setValue(self._default_x)
        self._ui.Ysize.setValue(self._default_y)

    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Reset the value to its default to not mess up the loading
        DO NOT RENAME: Overloading function
        """
        self.restore_default()
        return super().reject()


class CustomInputFormCircularCenter(QtWidgets.QDialog):
    def __init__(self):
        super(CustomInputFormCircularCenter, self).__init__()
        self._ui = Ui_CircularCenterInput()
        self._ui.setupUi(self)

    @Slot()
    def restore_default(self):
        """
        Restore all values to initial state
        """
        print("restoring to default")
        self._ui.rmms1st.setValue(10)
        self._ui.rmms2nd.setValue(60)
        self._ui.rmms3rd.setValue(1)
        self._ui.sigma_value.setValue(2)

    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Reset the value to its default to not mesys up the loading
        DO NOT RENAME: Overloading function
        """
        self.restore_default()
        return super().reject()


class CustomInputRemoveAperture(QtWidgets.QDialog):
    def __init__(self):
        super(CustomInputRemoveAperture, self).__init__()
        self._ui = Ui_RemoveAperture()
        self._ui.setupUi(self)

    @Slot()
    def restore_default(self):
        """
        Restore all values to initial state
        """
        print("restoring to default")
        self._ui.sigma_val.setValue(0)
        self._ui.add_radius.setValue(8)
        self._ui.aaf.setValue(2)

    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Reset the value to its default to not mess up the loading
        DO NOT RENAME: Overloading function
        """
        self.restore_default()
        return super().reject()


class CustomInputFormCenterOfMass(QtWidgets.QDialog):
    def __init__(self):
        super(CustomInputFormCenterOfMass, self).__init__()
        self._ui = Ui_CenterofMass()
        self._ui.setupUi(self)

    @Slot()
    def restore_default(self):
        """
        Restore all values to initial state
        """
        print("restoring to default")
        self._ui.nr.setValue(16)
        self._ui.nc.setValue(16)

    @Slot()
    def reject(self):
        """
        Overload of the reject function
        Reset the value to its default to not mess up the loading
        DO NOT RENAME: Overloading function
        """
        self.restore_default()
        return super().reject()


class CustomLoadingFormCenterOfMass(QtWidgets.QDialog):
    def __init__(self, ds_sel):
        """
        Set up a loading form with 1 progress bar parameters
        """
        super(CustomLoadingFormCenterOfMass, self).__init__()
        self._ui = Ui_LoadingBoxCenterOfMass()
        self._ui.setupUi(self)
        self.ds_sel = ds_sel

        self._center_of_mass = None
        self._ui.centerProgress.setValue(0)
        self._ui.centerProgress.setMaximum(np.prod(self.ds_sel.shape[:-2]))
        worker = GuiUpdater(fpdp_new.center_of_mass, self.ds_sel, 16, 16)
        print(self._ui.centerProgress.value())
        worker.signals.finished.connect(self.completed)
        worker.signals.progress.connect(self.progress_fn)
        print(self._ui.centerProgress.value())
        worker.signals.result.connect(self.center_of_mass)

    @Slot()
    def center_of_mass(self, value):
        print("self._center_of_mass")
        self._center_of_mass = value

    @Slot()
    def completed(self):
        return super().done(True)

    @Slot(tuple)
    def progress_fn(self, value):
        self._ui.centerProgress.setValue(
            self._ui.centerProgress.value() + value[0])
        print(self._ui.centerProgress.value())


class CustomLoadingForm(QtWidgets.QDialog):
    def __init__(self, ds_sel):
        """
        Set up a new loading form with 2 progress bar
        Parameters
        ----------
        ds_sel : MerlinBinary Memory Map

        """
        super(CustomLoadingForm, self).__init__()
        self._ui = Ui_LoadingBox()
        self._ui.setupUi(self)
        self.ds_sel = ds_sel
        self._sum_im = None
        self._sum_dif = None
        # set min and max value (Based on their code)
        self._ui.realProgress.setValue(0)
        self._ui.realProgress.setMinimum(0)
        self._ui.realProgress.setMaximum(np.prod(self.ds_sel.shape[:-2]))
        self._ui.recipProgress.setValue(0)
        self._ui.recipProgress.setMinimum(0)
        self._ui.recipProgress.setMaximum(np.prod(self.ds_sel.shape[:-2]))

        # create 2 thread and assign them signals based on the custum signals classes
        # First paramenter is the return value and second the fnct to call
        # Other are argument to pass to the function
        self._nb_thread = 2
        self.threadpool = QThreadPool()
        worker = GuiUpdater(fpdp_new.sum_im, self.ds_sel, 16, 16)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        worker.signals.result.connect(self.sum_im)

        self.threadpool.start(worker)

        worker2 = GuiUpdater(fpdp_new.sum_dif, self.ds_sel, 16, 16)
        worker2.signals.finished.connect(self.thread_complete)
        worker2.signals.progress.connect(self.progress_fn)
        worker2.signals.result.connect(self.sum_dif)

        self.threadpool.start(worker2)

    @Slot()
    def sum_im(self, value):
        print("self._sum_im")
        self._sum_im = value

    @Slot()
    def sum_dif(self, value):
        print("self._sum_dif")
        self._sum_dif = value

    @Slot(tuple)
    def progress_fn(self, value):
        """
        Update the progress on the bar depending on which function called it
        """
        if value[1] == "sum_diff":
            self._ui.recipProgress.setValue(
                self._ui.recipProgress.value() + value[0])

        else:
            self._ui.realProgress.setValue(
                self._ui.realProgress.value() + value[0])

    @Slot()
    def thread_complete(self):
        self._nb_thread -= 1
        if self._nb_thread == 0:  # Make sure both thread are done
            return super().done(True)


class CustomSignals(QObject):
    """
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

    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(tuple)


class GuiUpdater(QRunnable):
    """
    Worker thread
    """

    def __init__(self, fn, *args, **kwargs):
        super(GuiUpdater, self).__init__()
        # Store constructor arguments (re-used for processing)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.signals = CustomSignals()

        # Add the callback to our kwargs
        self._kwargs['progress_callback'] = self.signals.progress

    @Slot()  # QtCore.Slot
    def run(self):
        """
        run the function and return different signals based on the success or failure of the function
        """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result_val = self._fn(
                *self._args, **self._kwargs
            )
            print(result_val)
        except BaseException:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.result.emit(result_val)  # Done
            self.signals.finished.emit()  # Done
