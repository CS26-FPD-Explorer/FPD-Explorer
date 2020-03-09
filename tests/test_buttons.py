from pytestqt import qtbot
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QCoreApplication
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from fpd_explorer.data_browser_explorer import DataBrowserWidget
from fpd_explorer.home import *
from fpd_explorer import config_handler as config
from fpd_explorer.custom_widgets import CustomInputForm
from pynput.keyboard import Key, Controller
import time
from fpd_explorer.fpd_functions import *
from fpd_explorer.phase_correlation_fncts import *


def interact():
    keyboard = Controller()
    keyboard.press(Key.enter)


def setup_tests(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    config.load_config()
    aw._dm3_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.dm3"
    aw._mib_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"
    aw.mib_path = r"C:\Users\User\Documents\Physics Images\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"
    QTimer.singleShot(5000, interact)
    aw.load_files()
    return aw


def test_circ_center_button(qtbot):
    aw = setup_tests(qtbot)

    # QTimer.singleShot(5000, interact)
    try:
        fpd_functions.find_circular_centre(aw)
    except:
        assert False
    assert True


def test_synthetic_aperture_button(qtbot):
    aw = setup_tests(qtbot)
    # QTimer.singleShot(5000, interact)
    fpd_functions.find_circular_centre(aw)
    # QTimer.singleShot(500, interact)
    try:
        fpd_functions.remove_aperture(aw)
    except:
        assert False
    assert True


def test_center_of_mass_button(qtbot):
    aw = setup_tests(qtbot)
    fpd_functions.find_circular_centre(aw)
    fpd_functions.remove_aperture(aw)
    try:
        fpd_functions.centre_of_mass(aw)
    except:
        assert False
    assert True


def test_ransac_button(qtbot):
    aw = setup_tests(qtbot)
    fpd_functions.find_circular_centre(aw)
    fpd_functions.remove_aperture(aw)
    fpd_functions.centre_of_mass(aw)
    try:
        fpd_functions.ransac_im_fit(aw)
    except:
        assert False
    assert True


def test_matching_images_button(qtbot):
    aw = setup_tests(qtbot)
    try:
        phase_correlation_fncts.find_matching_images(aw)
    except:
        assert False
    assert True


def test_phase_correlation(qtbot):
    aw = setup_tests(qtbot)
    phase_correlation_fncts.find_matching_images(aw)
    try:
        phase_correlation_fncts.phase_correlation(aw)
    except:
        assert False
    assert True


def test_disc_edge_sigma(qtbot):
    aw = setup_tests(qtbot)
    phase_correlation_fncts.find_matching_images(aw)
    try:
        phase_correlation_fncts.disc_edge_sigma(aw)
    except:
        assert False
    assert True
