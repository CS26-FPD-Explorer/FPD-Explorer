import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from test_buttons import setup_tests, enter
from fpd_explorer import logger
from fpd_explorer.logger import Flags
from fpd_explorer.frontend.home import ApplicationWindow
from PySide2 import QtWidgets
import fpd_explorer.config_handler as config
import pytest
from pytestqt import qtbot


def setup_logger_tests(qtbot):
    aw = ApplicationWindow()
    qtbot.addWidget(aw)
    logger.setup(aw._ui.log_text, aw)


def test_add_flags_wrong_type(qtbot):
    setup_logger_tests(qtbot)
    with pytest.raises(TypeError) as excinfo:
        logger.add_flag(5)
        assert "wrong type" in str(excinfo.value)


def test_add_flags_wrong_value(qtbot):
    setup_logger_tests(qtbot)
    with pytest.raises(AttributeError) as excinfo:
        logger.add_flag(Flags.wrongtype)
        assert "wrong val" in str(excinfo.value)


def test_add_correct_flag(qtbot):
    setup_logger_tests(qtbot)
    try:
        logger.add_flag(Flags.phase_matching)
        assert 1
    except:
        assert 0


def test_log_in_str(qtbot):
    setup_logger_tests(qtbot)
    with pytest.raises(TypeError) as excinfo:
        logger.log(5)
        assert "wrong type in string " in str(excinfo.value)


def test_if_all_needed_flag_type(qtbot):
    setup_tests(qtbot)
    with pytest.raises(AttributeError) as excinfo:
        logger.check_if_all_needed(Flags.wrongtype)
        assert "wrong type" in str(excinfo.value)


def test_if_all_needed_prerequisite(qtbot):
    setup_tests(qtbot)
    enter()
    assert logger.check_if_all_needed(Flags.center_mass) == False


def test_if_all_needed_correct_output_aperture(qtbot, capsys):
    setup_tests(qtbot)
    logger.check_if_all_needed(Flags.aperture, display=False)
    capture = capsys.readouterr()
    string_out = capture.out
    assert "The circular centre must be calculated" in string_out


def test_if_all_needed_correct_output_center_mass(qtbot, capsys):
    setup_tests(qtbot)
    logger.check_if_all_needed(Flags.center_mass, display=False)
    capture = capsys.readouterr()
    string_out = capture.out
    assert "The circular centre must be calculated" in string_out \
        and "The aperture must be calculated" in string_out


def test_if_all_needed_correct_output_init_vadf(qtbot, capsys):
    setup_tests(qtbot)
    logger.check_if_all_needed(Flags.vadf_init, display=False)
    capture = capsys.readouterr()
    string_out = capture.out
    assert "The Virtual Annular Dark Field must be initialised" in string_out \
