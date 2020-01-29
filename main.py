from __future__ import unicode_literals
from custom_widgets import *
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from ui_inputbox import Ui_InputBox
from fpd.fpd_file import MerlinBinary
import h5py
import sys

import matplotlib as plt
import matplotlib.style
from PySide2 import QtWidgets

import fpd_explorer.config_handler as config
import qdarkgraystyle
from fpd_explorer.home import ApplicationWindow

plt.use('Qt5Agg')


if __name__ == "__main__":
    config.load_config()
    fpd_app = QtWidgets.QApplication()
    dark_mode_config = config.get_config("dark_mode")
    if dark_mode_config:
        plt.style.use('dark_background')
        fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    window = ApplicationWindow(fpd_app,dark_mode_config)
    window.show()
    sys.exit(fpd_app.exec_())
    # qApp.exec_()
