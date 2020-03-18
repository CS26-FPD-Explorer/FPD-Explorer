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
from PySide2 import QtWidgets

# FPD Explorer
from .. import logger
from ..logger import Flags
from .custom_fpd_lib import virtual_annular as va
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import Pop_Up_Widget


def start_vadf(ApplicationWindow):

    if logger.check_if_all_needed(Flags.npz_loaded, display=False):
        params = UI_Generator(ApplicationWindow, va.VirtualAnnularImages, key_ignore=["data"])

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.vadf = va.VirtualAnnularImages(ApplicationWindow.npz_path, **params.get_result())
    else:  # No need for an elif because we want to handle all the case if the next if is false
        if logger.check_if_all_needed(Flags.circular_center):
            if logger.check_if_all_needed(Flags.files_loaded):
                if logger.check_if_all_needed(Flags.hdf5_usage, display=False):
                    ds = ApplicationWindow.ds
                else:
                    ds = ApplicationWindow.ds_sel
                ApplicationWindow.vadf_input.update({"ds": ds})
                try:
                    ApplicationWindow.vadf_input.update({"com_yx": ApplicationWindow.com_yx})
                except AttributeError:
                    pass
                key_add = {
                    "data": [
                        "multipleinput", list(ApplicationWindow.vadf_input.items()), """`data`
                        is the data to be processed, as defined in the fpd.fpd_processing.map_image_function"""]}
                try:
                    key_add.update({"cyx": ["length 2 iterable", tuple(ApplicationWindow.cyx),
                                            "Centre y, x pixel cooridinates"]
                                    })
                except AttributeError:
                    pass
                params = UI_Generator(ApplicationWindow, va.VirtualAnnularImages, key_ignore=["data"], key_add=key_add)
                if not params.exec():
                    # Procedure was cancelled so just give up
                    return

                ApplicationWindow.vadf = va.VirtualAnnularImages(**params.get_result())
        else:
            return
    logger.log("VADF initialized correctly", Flags.vadf_init)


def plot_vadf(ApplicationWindow):
    if ApplicationWindow.vadf_explorer is not None:
        ApplicationWindow._ui.tabWidget.setCurrentWidget(
            ApplicationWindow._ui.tabWidget.findChild(QtWidgets.QWidget, "VADF Explorer"))
        return

    if logger.check_if_all_needed(Flags.vadf_init):
        hdf5_usage = logger.check_if_all_needed(Flags.hdf5_usage, display=False)
        vadf_widget = Pop_Up_Widget(ApplicationWindow, "VADF Explorer")
        ApplicationWindow.vadf_explorer = True
        if hdf5_usage or logger.check_if_all_needed(Flags.files_loaded, display=False):
            ApplicationWindow.vadf.plot(nav_im=ApplicationWindow.sum_dif, widget=vadf_widget)
        else:
            ApplicationWindow.vadf.plot(widget=vadf_widget)


def annular_slice(ApplicationWindow):
    if logger.check_if_all_needed(Flags.vadf_init):
        params = UI_Generator(ApplicationWindow, ApplicationWindow.vadf_explorer.annular_slice)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()

        vadf = ApplicationWindow.vadf_explorer.annular_slice(**results)
        canvas = Pop_Up_Widget(ApplicationWindow, "Annular Slice")
        fig = canvas.setup_docking("Annular Slice")
        ax = fig.get_fig().subplots()
        ax.matshow(vadf)
