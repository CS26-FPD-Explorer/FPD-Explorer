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

from fpd_explorer.files_fncts import *

'''
# omitted due to memory loading error on the vm

def test_load_files(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    keyboard = Controller()

    # adding dm3 file
    #aw._dm3_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.dm3"
    aw._dm3_path = "C:\cs26\example-data\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.dm3"

    # adding mib file
    #aw.mib_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.mib"
    #aw._mib_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.mib"

    aw.mib_path = "C:\cs26\example-data\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"
    aw._mib_path = "C:\cs26\example-data\Transfer-wbJpeYPVBcfcov9N\\13_FeRh-Alisa_DW_diff_20um_115C.mib"

    def interact():
        keyboard.press(Key.enter)

    QTimer.singleShot(5000, interact)
    aw.load_files()

    assert logger.check_if_all_needed(Flags.files_loaded)
'''


def test_load_hdf5(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    keyboard = Controller()

    aw.hdf5_path = "/home/ubuntu/example-data/13_FeRh-Alisa_DW_diff_20um_115C.hdr"
    aw._ui.action_hdf5.trigger()

    assert logger.check_if_all_needed(Flags.files_loaded)

    aw.start_dbrowser()
    assert aw._ui.tabWidget.widget(1).findChild(QtWidgets.QComboBox, "colorMap").currentIndex() == 0


def test_load_hdf5(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    keyboard = Controller()

    aw.hdf5_path = "/home/ubuntu/example-data/4DSTEM_FeRh_element.hdf5"
    aw._ui.action_hdf5.trigger()

    assert logger.check_if_all_needed(Flags.files_loaded)


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
