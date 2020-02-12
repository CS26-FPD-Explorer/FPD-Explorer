import fpd
import scipy as sp
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDockWidget, QMainWindow

# FPD Explorer
from .custom_fpd_lib import dpc_explorer_class as dpc
from .res.ui_dpc_browser import Ui_DPC_Explorer_Widget


class DPC_Explorer_Widget(QtWidgets.QWidget):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered
    mainwindow : QMainWindow The main window in which the dock widget should get created

    """

    def __init__(self, ApplicationWindow, mainwindow):
        super(DPC_Explorer_Widget, self).__init__()
        self._ui = Ui_DPC_Explorer_Widget()
        self._ui.setupUi(self)
        self._widgets = [self._ui.widget, self._ui.widget_2,
                         self._ui.widget_3, self._ui.widget_4]
        self._docked_widgets = []
        self.application_window = ApplicationWindow
        self.main_window = mainwindow

    def _get_first_free_widget(self):
        """
        Return the first widget in the list of available widget
        """
        return self._widgets.pop(0)

    def setup_docking(self, name, location="Top", floating=True):
        """
        Initialize a dock widget with the given name
        Parameters
        ----------
        name : str the name of the dock widget window

        Return
        ---------
        widget : QWidget the widget inside of the dock widget or None if no widget available
        location : tuple Position where we want the docking to be
        """
        widget = self._get_first_free_widget()
        if widget is not None:
            dock = QDockWidget(name, self.application_window)
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
            # Only need that if we want
            # dock.setFloating(floating)
            self._docked_widgets.append(dock)
        return widget

    def close_handler(self):
        print('closing')
        for el in self._docked_widgets:
            el.close()

def start_dpc(ApplicationWindow):
    """
    Start the DPC Explorer and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """
    mainwindow = QMainWindow()
    dpc_explorer = DPC_Explorer_Widget(ApplicationWindow, mainwindow)

    bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    bt = sp.ndimage.rotate(bt, angle=0.0, axes=(-2, -1),
                           reshape=False, order=3, mode='constant', cval=0.0, prefilter=True)

    ApplicationWindow._ui.tabWidget.tabCloseRequested.connect(dpc_explorer.close_handler)
    tab_index = ApplicationWindow._ui.tabWidget.addTab(mainwindow, "DPC Explorer")
    ApplicationWindow._ui.tabWidget.setCurrentIndex(tab_index)

    DE = dpc.DPC_Explorer(bt, cyx=(0, 0), vectrot=125, gaus=0.0, pct=0.5, widget=dpc_explorer)

    # TODO implement error message
