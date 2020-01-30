import sys, traceback
import logging
import os
import time
from fpd_explorer import logger 

import matplotlib as plt
import matplotlib.style
from PySide2 import QtWidgets

import fpd_explorer.config_handler as config
import qdarkgraystyle
from fpd_explorer.home import ApplicationWindow

plt.use('Qt5Agg')

error_logger = logging.getLogger('fpd_logger')
# Configure logger to write to a file...

def fpd_exept_handler(type, value, tb):
    tmp_str = "Uncaught exception: {0}".format(str(value))
    #error_logger.exception(value)
    widget = QtWidgets.QMessageBox.critical(window, "ERROR",tmp_str)
    if not os.path.isdir(".log/"):
        os.mkdir(".log")
    current_time = time.localtime()
    current_time = time.strftime("%H-%M-%S", current_time)
    with open(".log/"+current_time+".txt", "w") as f:
        f.write("Error occured at : " + current_time +"\n\n")
        f.write(tmp_str + "\n\n")
        for el in traceback.format_tb(tb):
            f.write(el)
    logger.clear()


sys.excepthook = fpd_exept_handler  

if __name__ == "__main__":
    config.load_config()
    fpd_app = QtWidgets.QApplication()
    dark_mode_config = config.get_config("dark_mode")
    if dark_mode_config:
        plt.style.use('dark_background')
        fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    window = ApplicationWindow(fpd_app,dark_mode_config)
    logger.setup(window._ui.log_text, window)

    window.show()
    sys.exit(fpd_app.exec_())
    # qApp.exec_()
