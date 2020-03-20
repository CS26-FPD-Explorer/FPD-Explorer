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
import operator
from enum import Enum, auto

from PySide2 import QtGui, QtWidgets


class Flags(Enum):
    """
    Order of the lines matter. It should match the order of the flow decided.
    """
    files_loaded = auto()
    hdf5_usage = auto()
    npz_loaded = auto()
    circular_center = auto()
    aperture = auto()
    center_mass = auto()
    ransac_fit = auto()
    vadf_init = auto()
    phase_matching = auto()

    def __lt__(self, other):
        return self.value < other.value


text_input = None
app = None
start_text = "Start by loading files"

global_flags = {
    Flags.files_loaded: {
        "bool": False,
        "error": "<b>The files must be loaded</b> before this step can be taken.<br><br>",
        "needing": []
    },
    Flags.hdf5_usage: {
        "bool": False,
        "error": "",
        "needing": []
    },
    Flags.npz_loaded: {
        "bool": False,
        "error": "",
        "needing": []
    },
    Flags.circular_center: {
        "bool": False,
        "error": "<b>The circular centre must be calculated</b> before this step can be taken.<br><br>",
        "needing": [Flags.files_loaded]
    },
    Flags.aperture: {
        "bool": False,
        "error": "<b>The aperture must be calculated</b> before this step can be taken.<br><br>",
        "needing": [Flags.files_loaded, Flags.circular_center]
    },
    Flags.center_mass: {
        "bool": False,
        "error": "<b>The center of mass must be calculated</b> before this step can be taken.<br><br>",
        "needing": [Flags.files_loaded, Flags.circular_center, Flags.aperture]
    },
    Flags.ransac_fit: {
        "bool": False,
        "error": "<b>The image must be fitted using ransac</b> before this step can be taken.<br><br>",
        "needing": [Flags.files_loaded, Flags.circular_center, Flags.aperture, Flags.center_mass]
    },
    Flags.vadf_init: {
        "bool": False,
        "error": "<b>The Virtual Annular Dark Field must be initialised </b> before this step can be taken.<br><br>",
        "needing": []
    },
    Flags.phase_matching: {
        "bool": False,
        "error": "<b>Matching images must have been found </b> before this step can be taken.<br><br>",
        "needing": [Flags.files_loaded]
    }
}


def setup(widget, application):
    global text_input, app
    text_input = widget
    app = application


def add_flag(flag: Flags):
    """
    Sets a flag to true for a given Flag type.

    Parameters
    ----------
    flag: Flags : Enum
    """

    if not isinstance(flag, Flags):
        raise TypeError
    val = global_flags.get(flag, None)
    if val is None:
        raise KeyError
    else:
        global_flags[flag]["bool"] = True


def log(in_str: str, flag: Flags = None):
    if text_input:
        if not isinstance(in_str, str):
            raise TypeError
        if flag:
            add_flag(flag)
        if start_text in text_input.toPlainText():
            text_input.clear()
        text_input.appendPlainText(in_str)
        text_input.moveCursor(QtGui.QTextCursor.End)
    else:
        raise RuntimeError("Text input is not defined")


def check_if_all_needed(current_flag: Flags, recursion: bool = False, display=True) -> bool:
    """
    Checks recursively all the flags necessary to run a function.
    If a function has prerequisites which has prerequites too, then they are found.
    If display is set to False, there is no pop-up which makes it easier/faster to test.

    Parameters
    ----------
    current_flag: Flags : Enum
    recursion : bool
    display: bool
    """

    if app is None:
        raise RuntimeError("No app has been provided")
    if not isinstance(current_flag, Flags):
        raise TypeError
    flag = global_flags.get(current_flag, None)
    if flag is None:
        raise KeyError
    if isinstance(flag, dict):  # Should always be true
        need = [(current_flag, flag.get("bool", False))]
        for el in flag.get("needing", []):
            need.append((el, check_if_all_needed(el, recursion=True)))
        if all([el[1] for el in need]):
            return True
        if not recursion:
            need = sorted(need, key=operator.itemgetter(0))
            err = [global_flags.get(el[0]).get("error") for el in need if not global_flags.get(el[0]).get("bool")]
            if display:
                err = "".join(err)
                QtWidgets.QMessageBox.warning(app, "Warning", err)
            else:
                err = "\n".join(err)
                print(err)
        return False
    else:
        raise RuntimeError("An unknow error has happened. Have you modified the structure of global_flags?")


def clear():
    """
    Clears the log and writes the text 'Start by loading files'
    to the workflow section of the UI.
    """
    if text_input:
        text_input.setPlainText(start_text)
        for key in global_flags.keys():
            global_flags[key]["bool"] = False
    else:
        raise RuntimeError("Text input is not defined")
