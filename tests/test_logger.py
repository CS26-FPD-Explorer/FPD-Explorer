import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from fpd_explorer import logger
from fpd_explorer.logger import Flags
from fpd_explorer.frontend.home import ApplicationWindow
from PySide2 import QtWidgets
import fpd_explorer.config_handler as config
import pytest


def test_add_flags_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        logger.add_flag(5)
        assert "wrong type" in str(excinfo.value)


def test_add_flags_wrong_value():
    with pytest.raises(AttributeError) as excinfo:
        logger.add_flag(Flags.wrongtype)
        assert "wrong val" in str(excinfo.value)


def test_add_correct_flag():
    try:
        logger.add_flag(Flags.phase_matching)
        assert 1
    except:
        assert 0


def test_log_in_str():
    with pytest.raises(TypeError) as excinfo:
        logger.log(5)
        assert "wrong type in string " in str(excinfo.value)
