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
from PySide2.QtCore import Slot

# FPD Explorer
from .. import logger
from ..logger import Flags
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import Pop_Up_Widget
from .custom_fpd_lib.data_browser import DataBrowser
from ..frontend.res.ui_data_browser import Ui_DataBrowser


class DataBrowserWidget(QtWidgets.QWidget):
    """
    Initialize the required widget needed by Data Browser tab.
    """

    def __init__(self, ApplicationWindow):
        super(DataBrowserWidget, self).__init__()
        self._ui = Ui_DataBrowser()
        self._ui.setupUi(self)
        self.application_window = ApplicationWindow
        self.data_browser = None
        self._init_color_map()

    def setup_ui(self, shape: tuple):
        """
        Set up all default values for Data Browser.
        """
        # Set the value to default
        scanY, scanX = shape
        self._ui.navX.setValue(scanX // 64 if scanX // 64 != 0 else 1)
        self._ui.navY.setValue(scanY // 64 if scanY // 64 != 0 else 1)
        self._ui.navX.setMaximum(scanX)
        self._ui.navY.setMaximum(scanY)
        self._ui.colorMap.setCurrentIndex(0)

    def set_data_browser(self, data_browser):
        """
        Secure setter for the Data Browser variable.
        """
        self.data_browser = data_browser

    def get_nav(self):
        """
        Returns the navigation widget of Data Browser.
        """
        return self._ui.navigationWidget

    def get_diff(self):
        """
        Returns the diffraction widget of Data Browser.
        """
        return self._ui.diffractionWidget

    def _init_color_map(self):
        """
        Create the dictionnary to fill the color map index.
        Values given by matplotlib wiki.
        """

        for el in self.application_window.cmaps.values():
            for cmaps in el:
                self._ui.colorMap.addItem(cmaps)

    @Slot(str)
    def update_color_map(self, value: str):
        """
        Update the rectangle based on the value selected by the user.

        Parameters
        ----------
        value : str name of the color map

        """
        if self.data_browser:
            return self.data_browser.update_color_map(value)
        else:
            self.sender().setCurrentIndex(0)

    @Slot()
    def recenter_dif_plot(self):
        return self.data_browser.recenter_dif_plot()

    @Slot(int)
    def update_rect(self, value: int):
        """
        Update the rectangle based on the value selected by the QSpinBox.

        Parameters
        ----------
        value : int new value to set the rectangle to

        """
        if self.data_browser:
            return self.data_browser.update_rect(value, self.sender().objectName())
        else:
            self.sender().setValue(1)


def start_dbrowser(ApplicationWindow):
    """
    Start Data Browser and switch to its tab if the files are loaded.
    Otherwise display an error.

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """
    if ApplicationWindow.data_browser is not None:
        ApplicationWindow._ui.tabWidget.setCurrentIndex(ApplicationWindow.find_index_name("Data Browser"))
        return
    if logger.check_if_all_needed(Flags.files_loaded):
        ApplicationWindow.db_widget = DataBrowserWidget(ApplicationWindow)

        hdf5_usage = logger.check_if_all_needed(Flags.hdf5_usage, display=False)
        ApplicationWindow.nav_data_input.update({"None": None})
        ApplicationWindow.nav_data_input.update({"sum_im": ApplicationWindow.sum_im})
        try:
            ApplicationWindow.data_input.update({"hdf5": ApplicationWindow.hdf5_path})
        except AttributeError:
            ApplicationWindow.data_input.update({"ds_sel": ApplicationWindow.ds_sel})

        key_add = {
            "fpgn": [
                "multipleinput", list(ApplicationWindow.data_input.items()),
                """Navigation image. If None, this is taken as the sum image.
                For numpy arrays, it is calculated directly."""],
            "nav_im": [
                "multipleinput", list(ApplicationWindow.nav_data_input.items()),
                """hdf5 str, file, group, dataset, ndarray, or dask array.
                hdf5 filename, file, group or dataset, or numpy array,
                `MerlinBinary` object, or dask array."""],
        }
        # Only used to save data

        def DummyDataBrowser():
            pass
        params = UI_Generator(ApplicationWindow, DummyDataBrowser, key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            ApplicationWindow.data_browser = None
            return
        results = params.get_result()
        data = results.get("fpgn")
        new_data = data
        try:
            if data == ApplicationWindow.hdf5_path:
                new_data = ApplicationWindow.ds_sel
        except AttributeError:
            pass
        ApplicationWindow.db_widget.setup_ui(new_data.shape[:2])
        ApplicationWindow.data_browser = DataBrowser(**results,
                                                     widget_1=ApplicationWindow.db_widget._ui.navCanvas,
                                                     widget_2=ApplicationWindow.db_widget._ui.diffCanvas)
        db_tab = Pop_Up_Widget(ApplicationWindow, "Data Browser")
        db_tab.setup_docking_default(ApplicationWindow.db_widget.get_nav(), name="Nav Im")
        db_tab.setup_docking_default(ApplicationWindow.db_widget.get_diff(), name="Diff Im")

        ApplicationWindow.db_widget.set_data_browser(ApplicationWindow.data_browser)
        logger.log("Data Browser has been opened")
