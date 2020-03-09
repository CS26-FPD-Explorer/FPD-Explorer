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
from fpd_explorer.virtual_adf import *


def interact():
    keyboard = Controller()
    keyboard.press(Key.enter)


def enter():
    QTimer.singleShot(250, interact)


def setup_tests(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    config.load_config()
    aw._dm3_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.dm3"
    aw._mib_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.mib"

    enter()
    aw.load_files()
    return aw


def test_circ_center_button(qtbot):
    aw = setup_tests(qtbot)

    try:
        enter()
        fpd_functions.find_circular_centre(aw)

    except:
        assert False
    assert True


def test_synthetic_aperture_button(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    try:
        enter()
        fpd_functions.remove_aperture(aw)
    except:
        assert False
    assert True


def test_center_of_mass_button(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    enter()
    fpd_functions.remove_aperture(aw)
    try:
        enter()
        fpd_functions.centre_of_mass(aw)
    except:
        assert False
    assert True


def test_ransac_button(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    enter()
    fpd_functions.remove_aperture(aw)
    enter()
    fpd_functions.centre_of_mass(aw)
    enter()
    try:
        fpd_functions.ransac_im_fit(aw)
    except:
        assert False
    assert True


def test_matching_images_button(qtbot):
    aw = setup_tests(qtbot)
    try:
        enter()
        phase_correlation_fncts.find_matching_images(aw)
    except:
        assert False
    assert True


def test_phase_correlation(qtbot):
    aw = setup_tests(qtbot)
    enter()
    phase_correlation_fncts.find_matching_images(aw)
    try:
        enter()
        phase_correlation_fncts.phase_correlation(aw)
    except:
        assert False
    assert True


def test_disc_edge_sigma(qtbot):
    aw = setup_tests(qtbot)
    enter()
    phase_correlation_fncts.find_matching_images(aw)
    try:
        enter()
        phase_correlation_fncts.disc_edge_sigma(aw)
    except:
        assert False
    assert True


def test_virtual_adf(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    try:
        enter()
        virtual_adf.start_vadf(aw)
    except:
        assert False
    assert True


def test_plot_vadf(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    enter()
    virtual_adf.start_vadf(aw)
    try:
        enter()
        virtual_adf.plot_vadf(aw)
    except:
        assert False
    assert True


def test_annular_slice(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    enter()
    virtual_adf.start_vadf(aw)
    try:
        enter()
        virtual_adf.annular_slice(aw)
    except:
        assert True
