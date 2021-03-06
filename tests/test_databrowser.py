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
import time

from PySide2 import QtCore
from pytestqt import qtbot
from PySide2.QtCore import QTimer, QCoreApplication
from pynput.keyboard import Key, Controller

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
from fpd_explorer.frontend.home import *
from fpd_explorer.frontend.files_fncts import *
from fpd_explorer.frontend.custom_widgets import CustomInputForm
from fpd_explorer.backend.data_browser_explorer import DataBrowserWidget
from test_buttons import enter, interact, setup_tests


# omitted due to memory loading error on the vm, for local use only
def setup_databrowser_tests(qtbot):
    aw = ApplicationWindow()
    db = DataBrowserWidget(aw)
    qtbot.addWidget(db)
    return db


def test_load_files(qtbot):
    aw = setup_tests(qtbot)
    assert logger.check_if_all_needed(Flags.files_loaded)


def test_load_hdf5(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)
    config.load_config()

    aw.hdf5_path = "/home/ubuntu/example-data/4DSTEM_FeRh_element.hdf5"
    enter()
    aw._ui.action_hdf5.trigger()
    assert logger.check_if_all_needed(Flags.files_loaded)
    aw.start_dbrowser()
    assert aw._ui.tabWidget.widget(1).findChild(QtWidgets.QComboBox, "colorMap").currentIndex() == 0


def test_load_npz(qtbot):
    aw = setup_tests(qtbot)

    aw.npz_path = "/home/ubuntu/example-data/VirtualAnnularImages_20200305_185503.npz"
    aw._ui.action_npz.trigger()

    assert logger.check_if_all_needed(Flags.npz_loaded)


def test_init_color_map(qtbot):
    db = setup_databrowser_tests(qtbot)
    assert db._ui.colorMap.count() == 82


def test_get_diff(qtbot):
    db = setup_databrowser_tests(qtbot)
    assert db.get_diff() == db._ui.diffractionWidget


def test_get_nav(qtbot):
    db = setup_databrowser_tests(qtbot)
    assert db.get_nav() == db._ui.navigationWidget
