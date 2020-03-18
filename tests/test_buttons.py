# Standard Library
import os
import sys
import time

import pytest
from PySide2 import QtCore
from pytestqt import qtbot
from PySide2.QtCore import QTimer, QCoreApplication
from pynput.keyboard import Key, Controller
from fpd.fpd_file import MerlinBinary
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
from fpd_explorer import config_handler as config
from fpd_explorer.frontend.home import *
from fpd_explorer.backend import virtual_adf
from fpd_explorer.backend.dpc_explorer import start_dpc
from fpd_explorer.backend import fpd_functions 
from fpd_explorer.backend.custom_fpd_lib.fpd_file import get_memmap
from fpd_explorer.frontend.custom_widgets import CustomInputForm
from fpd_explorer.backend.data_browser_explorer import DataBrowserWidget
from fpd_explorer.backend import phase_correlation_fncts 


def interact():
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def enter(time_before_executing=300):
    """
    automates running functions on the UI

    Parameters
    ----------
    time_before_executing: time in milliseconds to wait before
    execution of interact
    """
    QTimer.singleShot(time_before_executing, interact)


def setup_tests(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    config.load_config()
    setattr(MerlinBinary, get_memmap.__name__, get_memmap)

    aw._mib_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.mib"
    aw._dm3_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.dm3"
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

@pytest.mark.skip
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

@pytest.mark.skip
def test_dpc_explorer(qtbot):
    aw = setup_tests(qtbot)
    enter()
    fpd_functions.find_circular_centre(aw)
    enter()
    fpd_functions.remove_aperture(aw)
    enter()
    fpd_functions.centre_of_mass(aw)
    try:
        enter()
        # dpc brings up two input UIs when rotate is true
        start_dpc(aw)
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


# test passes locally, runner does not have enough ram to run on hdf5 (no skipping)
def test_phase_correlation(qtbot):
    aw = setup_tests(qtbot)
    enter()
    phase_correlation_fncts.find_matching_images(aw)
    try:
        enter()
        phase_correlation_fncts.phase_correlation(aw, False)
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

# requires dm3 and mib (does not run on hf5)
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

# requires dm3 and mib (does not run on hf5)
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


# requires dm3 and mib (does not run on hf5)
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
