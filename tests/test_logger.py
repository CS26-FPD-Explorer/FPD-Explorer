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

import pytest
from PySide2 import QtWidgets
from pytestqt import qtbot

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
import fpd_explorer.config_handler as config
from fpd_explorer import logger
from fpd_explorer.logger import Flags
from fpd_explorer.frontend.home import ApplicationWindow
from test_buttons import setup_tests, enter


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
    assert "The circular centre must be calculated" \
        and "The aperture must be calculated" in string_out


def test_if_all_needed_correct_output_init_vadf(qtbot, capsys):
    setup_tests(qtbot)
    logger.check_if_all_needed(Flags.vadf_init, display=False)
    capture = capsys.readouterr()
    string_out = capture.out
    assert "The Virtual Annular Dark Field must be initialised" in string_out


def test_if_all_needed_correct_output_ransac_fit(qtbot, capsys):
    setup_tests(qtbot)
    logger.check_if_all_needed(Flags.ransac_fit, display=False)
    capture = capsys.readouterr()
    string_out = capture.out
    assert "The Virtual Annular Dark Field must be initialised" \
        and "The center of mass must be calculated"\
        and "The aperture must be calculated" in string_out
