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
import inspect
from collections import OrderedDict

from PySide2 import QtGui, QtWidgets
from fpd.fpd_file import MerlinBinary
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QMainWindow

# FPD Explorer
from . import fnct_slots, files_fncts
from .. import logger
from .. import config_handler as config
from .guide import get_guide
from ..logger import Flags
from .gui_generator import UI_Generator
from .custom_widgets import LoadingForm, CustomInputForm
from .res.ui_homescreen import Ui_MainWindow
from ..backend.custom_fpd_lib import fpd_processing as fpdp_new


class ApplicationWindow(QMainWindow):
    """
    Create the main window and connect the menu bar slots
    """

    def __init__(self, app=None, dark_mode_config=False):
        super(ApplicationWindow, self).__init__()
        self._setup_slot()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._init_arrays()
        self._setup_actions()
        self.app = app
        self.dark_mode_config = dark_mode_config
        self.tabs_variables = ["data_browser", "dpc_explorer", "vadf_explorer"]
        if dark_mode_config is not None:
            self._ui.dark_mode_button.setChecked(dark_mode_config)
        else:
            self._ui.dark_mode_button.deleteLater()

        self._last_path = config.get_config("file_path")
        self._files_loaded = False
        for name in self.tabs_variables:
            self.__dict__[name] = None
        self._setup_cmaps()
        # makes all tabs except Home closable
        self._ui.tabWidget.tabCloseRequested.connect(self._handle_tab_close)
        # PySide2.QtWidgets.QTabBar.ButtonPosition for 2nd argument, LeftSide doesn't work
        self._ui.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)

    def _setup_slot(self):
        fncts = [(x.__name__, x) for x in fnct_slots.__dict__.values() if inspect.isfunction(x)]
        fncts.extend([(x.__name__, x) for x in files_fncts.__dict__.values() if inspect.isfunction(x)])
        for name, fnct in fncts:
            setattr(ApplicationWindow, name, fnct)

    @Slot(int)
    def _handle_tab_close(self, idx):
        name = self._ui.tabWidget.tabBar().tabText(idx).lower().replace(" ", "_")
        #set the variable to none
        if name in self.tabs_variables:
            self.__dict__[name] = None
        while self._ui.tabWidget.widget(idx).layout().count():
            self._ui.tabWidget.widget(idx).layout().takeAt(0).widget().deleteLater()
        self._ui.tabWidget.removeTab(idx)
        self._ui.tabWidget.setCurrentIndex(0)

    def _setup_actions(self):
        self._ui.action_mib.triggered.connect(self.open_mib)
        self._ui.action_dm3.triggered.connect(self.open_dm3)
        self._ui.action_hdf5.triggered.connect(self.open_hdf5)
        self._ui.action_npz.triggered.connect(self.open_npz)
        self._ui.actionCenter_of_Mass.triggered.connect(self.centre_of_mass)
        self._ui.actionCircular_center.triggered.connect(self.find_circular_centre)
        self._ui.actionDPC_Explorer.triggered.connect(self.start_dpc_explorer)
        self._ui.actionSynthetic_Aperture.triggered.connect(self.synthetic_aperture)
        self._ui.actionData_Browser.triggered.connect(self.start_dbrowser)
        self._ui.actionLoad.triggered.connect(self.load_files)
        self._ui.actionRansac_Tool.triggered.connect(self.ransac_im_fit)
        self._ui.actionVADF_Explorer.triggered.connect(self.start_vadf)
        self._ui.action_navigating_loading.triggered.connect(lambda: self.guide_me("navigating_and_loading"))
        self._ui.action_functions.triggered.connect(lambda: self.guide_me("functions"))
        self._ui.action_about_us.triggered.connect(lambda: self.guide_me("about_us"))
        self._ui.action_about_software.triggered.connect(lambda: self.guide_me("about_software"))
        self._ui.action_live_coding.triggered.connect(lambda: self.guide_me("live_coding"))
        self._ui.actionLive_Code.triggered.connect(self.start_live_coding)

    def _setup_cmaps(self):
        self.cmaps = OrderedDict()
        self.cmaps['Perceptually Uniform Sequential'] = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']
        self.cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        self.cmaps['Sequential (2)'] = [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']
        self.cmaps['Diverging'] = [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        self.cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']
        self.cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                                     'Dark2', 'Set1', 'Set2', 'Set3',
                                     'tab10', 'tab20', 'tab20b', 'tab20c']
        self.cmaps['Miscellaneous'] = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                                       'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                                       'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

    @Slot()
    def guide_me(self, topic):
        """
        Displays a guide pop-up with the text based on the parameter topic.

        Parameters
        ----------
        topic : str
            Key to look up in the dictionary of guide topics.
        """
        message = QtWidgets.QDialog(self)

        message.setMinimumSize(self.minimumWidth() // 3, self.minimumHeight() // 2)
        message.resize(self.minimumWidth() // 2, self.minimumHeight() // 1.5)

        message.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        message.setSizeGripEnabled(True)
        widget = QtWidgets.QTextBrowser()
        widget.setOpenExternalLinks(True)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttons.accepted.connect(message.accept)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(buttons)
        message.setLayout(layout)
        widget.setHtml(get_guide(topic))
        font = QtGui.QFont()
        font.setPointSize(11)
        widget.setFont(font)
        message.setWindowTitle(topic.replace("_", " ").capitalize())
        message.show()

    def _update_last_path(self, new_path):
        self._last_path = "/".join(new_path.split("/")[:-1]) + "/"
        config.add_config({"file_path": self._last_path})

    def _init_arrays(self):
        self.dpc_input = {}
        self.circular_input = {}
        self.mass_input = {}
        self.ransac_input = {}
        self.matching_input = {}
        self.edge_input = {}
        self.ref_input = {}
        self.phase_input = {}
        self.vadf_input = {}
        self.data_input = {}
        self.nav_data_input = {}

    @Slot()
    def change_color_mode(self):
        dark_mode_config = self._ui.dark_mode_button.isChecked()
        if self.app is not None:
            if dark_mode_config:
                try:
                    import qdarkgraystyle
                    self.app.setStyleSheet(qdarkgraystyle.load_stylesheet())
                except:
                    pass
            else:
                self.app.setStyleSheet("")

        QtWidgets.QMessageBox.information(self, "Information",
                                          """Your settings have correctly been applied
        Note that some changes will need a restart""")
        config.add_config({"Appearence": {"dark_mode": dark_mode_config}})

    @Slot()
    def clear_files(self):
        """
        Clears all provided files and resets the file_loaded flag
        """
        if self._ui.mib_line.text():
            del self._mib_path
            self._ui.mib_line.clear()
        if self._ui.dm3_line.text():
            del self._dm3_path
            self._ui.dm3_line.clear()
        if self._ui.hdf5_line.text():
            del self.hdf5_path
            self._ui.hdf5_line.clear()
        if self._ui.npz_line.text():
            del self.npz_path
            self._ui.npz_line.clear()
        self._files_loaded = False
        try:
            del self.cyx
            del self.ap
        except Exception:
            pass
        for _ in range(self._ui.tabWidget.count() - 1):
            # 1 because every time a tab is removed, indices are reassigned
            self._ui.tabWidget.removeTab(1)
        for name in self.tabs_variables:
            self.__dict__[name] = None
        logger.clear()

    @Slot()
    def load_files(self):
        """
        setp up the databrowser and open the file if not present
        """
        x_value = None
        y_value = None
        if logger.check_if_all_needed(Flags.hdf5_usage, display=False):
            logger.log("Files loaded correctly", Flags.files_loaded)
            return
        # Cherk if Mib exist
        try:
            mib = self._mib_path
        except AttributeError:
            response = QtWidgets.QMessageBox.warning(
                self, "Warning",
                """<b>You have not provided a Merlin Binary file.</b>
                <br> Would you like to select one?""",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                valid = self.open_mib()  # load a .mib file and use it
                if not valid:  # user cancelled
                    return
            else:
                return

        mib = self._mib_path
        # Check if dm3 exist
        try:
            dm3 = self._dm3_path
        except AttributeError:
            dm3 = []
            response = QtWidgets.QMessageBox.warning(
                self, "Warning",
                """<b>You have not provided a Digital Micrograph file.</b>
                <br> Would you like to select one?""",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                if not self.open_dm3():  # user cancelled
                    return
                dm3 = self._dm3_path
            if response == QtWidgets.QMessageBox.No:
                logger.log("Working without a DM3 file")
                key_add = {
                    "scanXalu": ["int", 256, "Determines scan size if no `dmfns` are specified"],
                    "scanYalu": ["int", 256, "Determines scan size if no `dmfns` are specified"]
                }
                params = UI_Generator(self, None, key_add=key_add)
                if not params.exec():
                    # Procedure was cancelled so just give up
                    return
                results = params.get_result()
                x_value = (results["scanXalu"], 'x', 'na')
                y_value = (results["scanYalu"], 'y', 'na')

            if response == QtWidgets.QMessageBox.Cancel:
                return

        hdr = self._mib_path[:-4] + ".hdr"
        self.mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
                               scanXalu=x_value, row_end_skip=1)

        self.ds = self.mb.get_memmap()
        real_skip, recip_skip = self.input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                                                text_y="Amount to skip for Diffraction Image")

        self.ds_sel = self.ds[::real_skip,
                              ::real_skip, ::recip_skip, ::recip_skip]

        loading_widget = LoadingForm(2, ["sum_im", "sum_dif"])
        loading_widget.setup_multi_loading("sum_im", fpdp_new.sum_im, self.ds_sel, 16, 16)
        loading_widget.setup_multi_loading("sum_dif", fpdp_new.sum_dif, self.ds_sel, 16, 16)
        loading_widget.exec()
        self.sum_dif = loading_widget.get_result("sum_dif")
        self.sum_im = loading_widget.get_result("sum_im")
        self._files_loaded = True
        logger.log("Files loaded correctly", Flags.files_loaded)

    def input_form(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
        """
        create an input form with the given value

        Parameters
        ----------
        initial_x : int
            Value the top value should start from
        initial_y : int
            Value the bottom value should start from
        minimum : int
            Minimum value the spin box should be allowed to go
        maximum : int
            Maximum value the spin box should be allowed to go
        text_x : str
            Text to set in the top screen
        text_y : str
            Text to set in the bottom screen

        """

        widget = CustomInputForm(initial_x, initial_y,
                                 minimum, maximum, text_x, text_y)
        if not widget.exec():
            return
        x = pow(2, widget._ui.Xsize.value())
        y = pow(2, widget._ui.Ysize.value())
        return x, y

    def closeEvent(self, event):
        config.save_config()
        event.accept()
