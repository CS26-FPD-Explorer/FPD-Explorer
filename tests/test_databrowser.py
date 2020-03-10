from pytestqt import qtbot
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QCoreApplication
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from fpd_explorer.data_browser_explorer import DataBrowserWidget
from fpd_explorer.home import *
from test_buttons import setup_tests, enter, interact
from fpd_explorer.custom_widgets import CustomInputForm
from pynput.keyboard import Key, Controller
import time

from fpd_explorer.files_fncts import *


# omitted due to memory loading error on the vm
# for local use only

def test_load_files(qtbot):
    aw = setup_tests(qtbot)
    assert logger.check_if_all_needed(Flags.files_loaded)


def test_load_hdf5(qtbot):
    aw = setup_tests(qtbot)

    assert logger.check_if_all_needed(Flags.files_loaded)
    aw.start_dbrowser()

    assert aw._ui.tabWidget.widget(1).findChild(QtWidgets.QComboBox, "colorMap").currentIndex() == 0


def test_load_npz(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    keyboard = Controller()

    aw.npz_path = "/home/ubuntu/example-data/VirtualAnnularImages_20200305_185503.npz"
    #aw.npz_path = "C:\cs26\example-data\Transfer-wbJpeYPVBcfcov9N\\VirtualAnnularImages_20200305_185503.npz"
    aw._ui.action_npz.trigger()

    assert logger.check_if_all_needed(Flags.npz_loaded)


def test_init_color_map(qtbot):
    aw = ApplicationWindow()
    db = DataBrowserWidget(aw)
    qtbot.addWidget(db)
    assert db._ui.colorMap.count() == 54


def test_get_diff(qtbot):
    aw = ApplicationWindow()
    db = DataBrowserWidget(aw)
    qtbot.addWidget(db)
    assert db.get_diff() == db._ui.diffractionWidget


def test_get_nav(qtbot):
    aw = ApplicationWindow()
    db = DataBrowserWidget(aw)
    qtbot.addWidget(db)
    assert db.get_nav() == db._ui.navigationWidget
