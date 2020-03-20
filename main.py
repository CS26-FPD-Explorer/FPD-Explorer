# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

# Standard Library
import os
import sys
import logging
import traceback
from datetime import datetime

import matplotlib as plt
import matplotlib.style
from PySide2 import QtWidgets

# First Party
import fpd_explorer.config_handler as config
from fpd_explorer import logger
from fpd_explorer.frontend.home import ApplicationWindow

plt.use('Qt5Agg')

error_logger = logging.getLogger('fpd_logger')


def fpd_except_handler(type, value, tb):
    tmp_str = "An Exception has occured: \n{0}".format(str(value))
    err = ""
    for el in traceback.format_tb(tb):
        err += el + "\n"
    print(f"{value} \n {err}")
    widget = QtWidgets.QMessageBox.critical(window, "ERROR", tmp_str)
    write_log(tmp_str, err)


def write_log(error, tb):
    if not os.path.isdir(".log/"):
        os.mkdir(".log")
    remove_old_log()
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y@%H-%M-%S")
    with open(".log/" + current_time + ".txt", "w") as f:
        f.write("Error occured at : " + current_time + "\n\n")
        f.write(error + "\n\n")
        f.write(tb)


def remove_old_log():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(".log/"):
        f.extend([os.path.join(*dirpath.split("/"), s) for s in filenames])
    tmp = [el for el in f if el[-4:] == ".txt"]
    len_tmp = len(tmp)
    if len_tmp >= 10:
        for el in sorted(tmp, reverse=True)[9:]:
            os.remove(el)


sys.excepthook = fpd_except_handler

if __name__ == "__main__":
    config.load_config()
    fpd_app = QtWidgets.QApplication()
    dark_mode_config = config.get_config("dark_mode")
    try:
        import qdarkgraystyle
        if dark_mode_config:
            plt.style.use('dark_background')
            fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    except ImportError:
        dark_mode_config = None
    window = ApplicationWindow(fpd_app, dark_mode_config)
    logger.setup(window._ui.log_text, window)
    window.show()
    sys.exit(fpd_app.exec_())
