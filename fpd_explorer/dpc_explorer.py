from .custom_fpd_lib import dpc_explorer_class as dpc
import scipy as sp
from .res.ui_dpc_browser import Ui_DPC_Explorer_Widget
import fpd

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QDockWidget, QMainWindow


class DPC_Explorer_Widget(QtWidgets.QWidget):
    def __init__(self, ApplicationWindow, mainwindow):
        super(DPC_Explorer_Widget, self).__init__()
        self._ui = Ui_DPC_Explorer_Widget()
        self._ui.setupUi(self)
        self.widgets = [self._ui.widget, self._ui.widget_2,
                        self._ui.widget_3, self._ui.widget_4]

        self.application_window = ApplicationWindow
        self.main_window=mainwindow

    def _get_first_free_widget(self):
        return self.widgets.pop(0)

    def setup_docking(self, name):
        widget = self._get_first_free_widget()
        dock = QDockWidget(name, self.application_window)
        dock.setWidget(widget)
        self.main_window.addDockWidget(Qt.TopDockWidgetArea, dock)
        return widget


def start_dpc(ApplicationWindow):
    mainwindow = QMainWindow()
    dpc_explorer = DPC_Explorer_Widget(ApplicationWindow, mainwindow)

    bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    bt = sp.ndimage.rotate(bt, angle=0.0, axes=(-2, -1), 
        reshape=False, order=3, mode='constant', cval=0.0, prefilter=True)

    tab_index = ApplicationWindow._ui.tabWidget.addTab(mainwindow, "DPC Explorer")
    ApplicationWindow._ui.tabWidget.setCurrentIndex(tab_index)
    
    DE = dpc.DPC_Explorer(bt, cyx=(0, 0), vectrot=125, gaus=0.0, pct=0.5, widget=dpc_explorer)

