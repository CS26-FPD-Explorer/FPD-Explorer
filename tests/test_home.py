import pytest
from pytestqt import qtbot
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QCoreApplication
import sys
import os
from fpd_explorer.data_browser_explorer import DataBrowserWidget
from fpd_explorer.home import *
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")


def test_clear_files(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    aw.clear_files()
    assert aw._files_loaded == False
    assert aw._cyx == None
    assert aw._ap == None
    with pytest.raises(AttributeError) as excinfo:
        aw._mib_path is None == True
        aw._dm3_path is None == True
        assert "self._mib_path and self._dm3_path have been deleted" in str(excinfo.value)
    assert aw._ui.mib_line.text() == ''
    assert aw._ui.dm3_line.text() == ''