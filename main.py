import sys

import matplotlib as plt
import matplotlib.style
from PySide2 import QtWidgets

import FPD_Explorer.config_handler as config
import qdarkgraystyle
from FPD_Explorer.home import ApplicationWindow

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
