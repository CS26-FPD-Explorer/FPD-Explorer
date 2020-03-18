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

import fpd
import scipy as sp
from PySide2 import QtWidgets

# FPD Explorer
from .custom_fpd_lib import dpc_explorer_class as dpc
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import Pop_Up_Widget


def start_dpc(ApplicationWindow):
    """
    Start the DPC Explorer and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QApplication
        Parent in which the tab should be rendered

    """
    if ApplicationWindow.dpc_explorer is not None:
        ApplicationWindow._ui.tabWidget.setCurrentWidget(
            ApplicationWindow._ui.tabWidget.findChild(QtWidgets.QWidget, "DPC Explorer"))
        return
    ApplicationWindow.dpc_explorer = Pop_Up_Widget(ApplicationWindow, "DPC Explorer")

    try:
        ApplicationWindow.dpc_input.update({"com_yx_beta": ApplicationWindow.com_yx_beta})
    except AttributeError:
        pass

    try:
        ApplicationWindow.dpc_input.update({"ransac": ApplicationWindow.com_yx_cor})
    except AttributeError:
        pass
    try:
        ApplicationWindow.dpc_input.update({"beta2bt": fpd.mag_tools.beta2bt(
            ApplicationWindow.com_yx_cor) * 1e9})

    except AttributeError:
        pass

    if len(ApplicationWindow.dpc_input) == 0:
        ApplicationWindow.dpc_explorer = None
        raise Exception("""No data found that could be used with DPC Explorer.\n
        Please run some function before trying again""")
    key_add = {
        "d": [
            "multipleinput", list(ApplicationWindow.dpc_input.items()), """If array-like, yx data. If length 2 iterable or ndarray of \n
                    shape (2, M, N), data is single yx dataset. If shape is \n
                    (S, 2, M, N), a sequence yx data of length S can be plotted."""],
        "rotate": [
            "bool", False, "rotate image if needed. This can make data interpretation easier"],
        "hist_lims": [
            "togglevalue", ["length4tupleofscalars,orNone", None,
                            """Histogram limits in order of xmin, xmax, ymin, ymax.\n
                                If None, limits are taken from data."""],
            """Check if you want to manually set the hist lim"""],
        "descan": [
            "togglevalue", ["length 4 iterable", [0, 0, 0, 0], """Plane descan correction.\n
                            [Yy, Yx, Xy, Xx] entered in 1/1000 for for convenience."""],
            """Check if you want to manually set the descan"""
        ]}
    try:
        key_add.update({"cyx": ["length 2 iterable", tuple(ApplicationWindow.cyx),
                                "Centre y, x pixel cooridinates"]
                        })
    except AttributeError:
        pass

    params = UI_Generator(ApplicationWindow, dpc.DPC_Explorer, key_ignore=[
                          "r_min", "r_max", "median", "flip_y", "flip_x", "ransac"], key_add=key_add)
    if not params.exec():
        # Procedure was cancelled so just give up
        return
    results = params.get_result()
    # bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    if results.pop("rotate"):
        rot_params = UI_Generator(ApplicationWindow, sp.ndimage.rotate, key_ignore=["input"])
        if not rot_params.exec():
            # Procedure was cancelled so just give up
            return
        rot_results = rot_params.get_result()
        rot_results["axes"] = (int(rot_results["axes"][0]), int(rot_results["axes"][1]))
        results["d"] = sp.ndimage.rotate(results["d"], **rot_results)
    DE = dpc.DPC_Explorer(**results, widget=ApplicationWindow.dpc_explorer)
