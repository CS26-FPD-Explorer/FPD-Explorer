# Standard Library
import sys
import traceback
from collections import defaultdict

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QObject, QThread, QThreadPool
from matplotlib.figure import Figure
from PySide2.QtWidgets import QDockWidget, QMainWindow, QVBoxLayout
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_ipython_widget import RichIPythonWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# FPD Explorer
from .res.ui_inputbox import Ui_InputBox


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, figsize=None):
        self._fig = Figure(figsize=figsize)

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

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        buttonBox.rejected.connect(lambda: self.application_window._ui.tabWidget.tabCloseRequested.emit(
            self.application_window._ui.tabWidget.currentIndex()))
        buttonBox.button(QtWidgets.QDialogButtonBox.Close).setDefault(True)

        self.gridLayout = QVBoxLayout()
        self.gridLayout.addWidget(self.main_window)
        self.gridLayout.addWidget(buttonBox)
        self.main_widget.setLayout(self.gridLayout)

        self._docked_widgets = []
        # self.application_window._ui.tabWidget.tabCloseRequested.connect(self.close_handler)

    def setup_docking(self, name, location="Top", figsize=None):
        """
        Initialize a dock widget with the given name
        Parameters
        ----------
        name : str the name of the dock widget window

        Return
        ---------
        widget : QWidget the widget inside of the dock widget
        """
        widget = MyMplCanvas(self, figsize)
        return self.setup_docking_default(widget, location)

    def setup_docking_default(self, widget, location="Top"):
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


class LoadingForm(QtWidgets.QDialog):
    def __init__(self, nb_bar, name, *args, **kwargs):
        """
        Set up a loading form with 1 progress bar parameters
        """
        super(LoadingForm, self).__init__()
        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)

        self.data_out = defaultdict(list)
        self.threadpool = QThreadPool()
        # self._ui.centerProgress.setMaximum(np.prod(data.shape[:-2]))
        self.nb_threads = nb_bar
        for el in range(nb_bar):
            self.setup_ui(name[el])
        self.v_layout.addWidget(cancel_button)
        self.resize(self.width(), self.minimumHeight())

    def setup_ui(self, name):
        widget = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout()
        self.data_out[name].insert(0, None)
        bar = QtWidgets.QProgressBar()
        bar.setValue(0)
        self.data_out[name].insert(1, bar)
        form.addRow(name, bar)
        widget.setLayout(form)
        self.v_layout.addWidget(widget)

    def setup_multi_loading(self, name, fnct, *args, **kwargs):
        worker = GuiUpdater(fnct, name, *args, **kwargs)
        worker.signals.finished.connect(self.completed)
        worker.signals.progress.connect(self.progress_func)
        worker.signals.result.connect(self.set_value)
        worker.signals.maximum.connect(self.set_max)
        if isinstance(name, str):
            name = [name]
        for el in range(len(name)):
            self.data_out[name[el]].append(worker)
        worker.start()

    @Slot()
    def set_max(self, obj):
        name, max_size = obj
        self.data_out[name][1].setMaximum(max_size)

    @Slot()
    def set_value(self, obj):
        self.data_out[obj[0]][0] = obj[1]

    def setup_loading(self, name, max_size):
        self.set_max(name, max_size)
        return self.data_out[name][-1].signals.progress

    @Slot()
    def cancel(self):
        return super().done(False)

    @Slot()
    def completed(self):
        self.nb_threads -= 1
        if self.nb_threads == 0:
            return super().done(True)

    @Slot(tuple)
    def progress_func(self, obj):
        self.data_out[obj[0]][1].setValue(self.data_out[obj[0]][1].value() + obj[1])

    def get_result(self, name):
        return self.data_out[name][0]


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
    maximum = Signal(tuple)


class GuiUpdater(QThread):
    """
    Worker thread
    """

    def __init__(self, fn, name, *args, **kwargs):
        super(GuiUpdater, self).__init__()
        # Store constructor arguments (re-used for processing)
        self._fn = fn
        self._name = name
        self._args = args
        self._kwargs = kwargs
        self.signals = CustomSignals()

        # Add the callback to our kwargs
        self._kwargs['callback'] = self.signals

    @Slot()  # QtCore.Slot
    def run(self):
        """
        run the function and return different signals based on the success or failure of the function
        """
        # Retrieve args/kwargs here; and fire processing using them
        result_val = None
        try:
            result_val = self._fn(
                *self._args, **self._kwargs
            )
        except BaseException:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.result.emit((self._name, result_val))  # Done
            self.signals.finished.emit()  # Done


class QIPythonWidget(RichIPythonWidget):
    """ Convenience class for a live IPython console widget."""

    def __init__(self, ApplicationWindow=None, customBanner=None, *args, **kwargs):
        super(QIPythonWidget, self).__init__(*args, **kwargs)
        if customBanner is not None:
            self.banner = customBanner
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_manager.kernel.gui = 'qt'
        self.kernel_client = self._kernel_manager.client()
        self.kernel_client.start_channels()
        self.kernel_manager.kernel.shell.push({"fpd_app": ApplicationWindow})

        def stop():
            self.kernel_client.stop_channels()
            self.kernel_manager.shutdown_kernel()
        self.exit_requested.connect(stop)

    def pushVariables(self, variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        print(variableDict)
        self.kernel_manager.kernel.shell.push(variableDict)

    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()

    def printText(self, text):
        """ Prints some plain text to the console """
        self._append_plain_text(text)

    def executeCommand(self, command):
        """ Execute a command in the frame of the console widget """
        self._execute(command, True)
