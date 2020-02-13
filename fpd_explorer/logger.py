# Standard Library
import operator
from enum import Enum, auto

from PySide2 import QtWidgets


class Flags(Enum):
    """
    Order of the lines matter. It should match the order of the flow decided
    """
    files_loaded = auto()
    circular_center = auto()
    aperture = auto()
    center_mass = auto()

    def __lt__(self, other):
        return self.value < other.value


text_input = None
app = None

global_flags = {
    Flags.files_loaded: {
        "bool": False,
        "error": "<b>The files must be loaded</b> before the aperture can be generated.<br><br>",
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
    }
}


def setup(widget, application):
    global text_input, app
    text_input = widget
    app = application


def add_flag(flag: Flags):
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
        text_input.appendPlainText(in_str)
    else:
        raise RuntimeError("Text Input is not Defined")


def check_if_all_needed(current_flag: Flags, recursion: bool = False, display=True) -> bool:
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
            print(err)
            if display:
                err = "".join(err)
                QtWidgets.QMessageBox.warning(app, "Warning", err)
            else:
                err = "\n".join(err)
                print(err)
        return False
    else:
        raise RuntimeError("An unknow error has happened. Did you modified the structure of globals_flags")


def clear(self):
    if text_input:
        text_input.setPlainText("")
        for key in global_flags.keys():
            global_flags[key]["bool"] = False
    else:
        raise RuntimeError("Text Input is not Defined")
