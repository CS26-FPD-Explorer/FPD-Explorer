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

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# First Party
from fpd_explorer.frontend.custom_widgets import CustomInputForm


def init_inputbox():
    """
    Create an inputbox.ui similar to those used to scale the size of the input data.
    """
    return CustomInputForm(initial_x=2, initial_y=2, minimum=0, maximum=13, text_x='', text_y='')


def test_input_form_size_maximum(qtbot):
    """
    Test Xsize and Ysize have a maximum value set. This means that we cannot reduce the size
    of the data by large amounts affecting the quality of the visualisation produced.
    """
    widget = init_inputbox()
    widget._ui.Xsize.setValue(14)
    widget._ui.Ysize.setValue(14)
    assert (widget._ui.Xsize.value() > widget._ui.Xsize.maximum()) == False
    assert (widget._ui.Ysize.value() > widget._ui.Ysize.maximum()) == False


def test_input_form_restore_to_default(qtbot):
    """
    Test if the restore to default function that is bound to the Restore Default
    button resets the values correctly.
    """
    widget = init_inputbox()
    widget._ui.Xsize.setValue(10)
    widget._ui.Ysize.setValue(10)
    widget.restore_default()
    assert widget._ui.Xsize.value() == 2
    assert widget._ui.Ysize.value() == 2
