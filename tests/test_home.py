# Standard Library
import os
import sys

import pytest
from PySide2 import QtCore
from pytestqt import qtbot
from PySide2.QtCore import QTimer, QCoreApplication
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
from fpd_explorer.frontend.home import *
from fpd_explorer.backend.data_browser_explorer import DataBrowserWidget



def test_clear_files(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)

    aw.clear_files()
    assert aw._files_loaded == False
    assert aw.cyx == None
    assert aw.ap == None
    with pytest.raises(AttributeError) as excinfo:
        aw._mib_path is None == True
        aw._dm3_path is None == True
        assert "self._mib_path and self._dm3_path have been deleted" in str(excinfo.value)
    assert aw._ui.mib_line.text() == ''
    assert aw._ui.dm3_line.text() == ''
