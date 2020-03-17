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

import pytest
from pytestqt import qtbot
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QCoreApplication
import sys
import os
from fpd_explorer.backend.data_browser_explorer import DataBrowserWidget
from fpd_explorer.frontend.home import *
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")


def test_clear_files(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)

    aw.clear_files()
    assert aw._files_loaded == False
    with pytest.raises(AttributeError) as excinfo:
        aw._mib_path is None == True
        aw._dm3_path is None == True
        assert "self._mib_path and self._dm3_path have been deleted" in str(excinfo.value)
    assert aw._ui.mib_line.text() == ''
    assert aw._ui.dm3_line.text() == ''
