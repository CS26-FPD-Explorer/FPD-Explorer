import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from fpd_explorer import logger
from fpd_explorer.frontend.home import ApplicationWindow
from PySide2 import QtWidgets
import fpd_explorer.config_handler as config
import pytest


def test_add_flags_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        logger.add_flag(5)
        assert "wrong type" in str(excinfo.value)
