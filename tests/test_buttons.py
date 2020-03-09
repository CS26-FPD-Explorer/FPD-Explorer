from pytestqt import qtbot
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QCoreApplication
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from fpd_explorer.data_browser_explorer import DataBrowserWidget
from fpd_explorer.home import *

from fpd_explorer.custom_widgets import CustomInputForm
from pynput.keyboard import Key, Controller
import time
from fpd_explorer.fpd_functions import *


def interact():
    keyboard = Controller()
    keyboard.press(Key.enter)


def setup_tests(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)

    aw._dm3_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.dm3"
    aw._mib_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"
    aw.mib_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"
    QTimer.singleShot(5000, interact)
    aw.load_files()
    return aw


def test_circ_center_button(qtbot):
    aw = setup_tests(qtbot)

    QTimer.singleShot(5000, interact)
    try:
        fpd_functions.find_circular_centre(aw)
    except:
        assert False
    assert True


# def test_synthetic_aperture_button(qtbot):
    aw = setup_tests(qtbot)
