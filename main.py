import logging
import os
import sys
import traceback
from datetime import datetime

import matplotlib as plt
import matplotlib.style
from PySide2 import QtWidgets

import fpd_explorer.config_handler as config
import qdarkgraystyle
from fpd_explorer import logger
from fpd_explorer.home import ApplicationWindow

plt.use('Qt5Agg')

error_logger = logging.getLogger('fpd_logger')
# Configure logger to write to a file...


def fpd_exept_handler(type, value, tb):
    tmp_str = "Uncaught exception: {0}".format(str(value))
    # error_logger.exception(value)
    widget = QtWidgets.QMessageBox.critical(window, "ERROR", tmp_str)
    write_log(tmp_str, tb)
    logger.clear()


def write_log(error, tb):
    if not os.path.isdir(".log/"):
        os.mkdir(".log")
    remove_old_log()
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y@%H-%M-%S")
    with open(".log/" + current_time + ".txt", "w") as f:
        f.write("Error occured at : " + current_time + "\n\n")
        f.write(error + "\n\n")
        for el in traceback.format_tb(tb):
            f.write(el)


def remove_old_log():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(".log/"):
        f.extend([os.path.join(*dirpath.split("/"), s) for s in filenames])
    tmp = [el for el in f if el[-4:] == ".txt"]
    len_tmp = len(tmp)
    if len_tmp >= 10:
        print(sorted(tmp))
        for el in sorted(tmp, reverse=True)[9:]:
            print("removing", el)
            os.remove(el)


sys.excepthook = fpd_exept_handler

if __name__ == "__main__":
    config.load_config()
    fpd_app = QtWidgets.QApplication()
    dark_mode_config = config.get_config("dark_mode")
    if dark_mode_config:
        plt.style.use('dark_background')
        fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    window = ApplicationWindow(fpd_app, dark_mode_config)
    logger.setup(window._ui.log_text, window)

    window.show()
    sys.exit(fpd_app.exec_())
    # qApp.exec_()
