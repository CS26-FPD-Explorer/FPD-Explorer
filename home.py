from __future__ import unicode_literals
import sys
import os
import matplotlib
import random
import numpy as np
import scipy as sp
import h5py

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot

from fpd.fpd_file import MerlinBinary

from ui_homescreen import Ui_MainWindow
from ui_inputbox import Ui_InputBox
# from ui_mainwindow import Ui_MainWindow
from DataBrowserNew import DataBrowserNew
from custom_widgets import *

os.environ["OMP_NUM_THREADS"] = "1"

# Make sure that we are using QT5

# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets
matplotlib.use('Qt5Agg')
# progname = os.path.basename(sys.argv[0])
progversion = "0.1"
os.environ["OMP_NUM_THREADS"] = "1"


class ApplicationWindow(QMainWindow):
    """
    Create the main window and connect the menu bar slots
    """

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.action_mib.triggered.connect(self.function_mib)
        # self._ui.action_dm3.triggered.connect(self.function_dm3)
        # self._ui.action_hdf5.triggered.connect(self.function_hdf5)
        # self._ui.action_about.triggered.connect(self.function_about)

        self._data_browser = None
        self._last_path = ""

    @Slot()
    def function_mib(self):
        """
        Spawn a file dialog to open an mib file
        """
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path, "MERLIN binary files (*.mib)")
        if fname:
            if fname[-3:] == "mib":  # empty string means user cancelled
                self._last_path = fname
                self._mib_path = fname
                self._ui.mib_line.clear()
                self._ui.mib_line.insert(fname[fname.rfind('/') + 1 :])
                return True
        return False

    # @Slot()
    # def LoadFiles(self):
    #     x_value = None
    #     y_value = None
    #     #Cherk if Mib exist
    #     try:
    #         mib = self.mib_path
    #     except AttributeError:
    #         response = QtWidgets.QMessageBox.warning(
    #             self, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
    #             QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #             QtWidgets.QMessageBox.Yes)
    #         if response == QtWidgets.QMessageBox.Yes:
    #             valid = self.function_mib()  # load a .mib file and use it
    #             if not valid: #user canceled
    #                 return 
    #         else:
    #             return


fpd_app = QtWidgets.QApplication()

window = ApplicationWindow()
# window.setWindowTitle("%s" % progname)
window.show()
sys.exit(fpd_app.exec_())
# qApp.exec_()
