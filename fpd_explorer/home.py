
# Standard Library
import inspect
from collections import OrderedDict

import qdarkgraystyle
from PySide2 import QtWidgets
from fpd.fpd_file import MerlinBinary
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow

# FPD Explorer
from . import logger, fnct_slots, files_fncts, virtual_adf, dpc_explorer, fpd_functions
from . import config_handler as config
from . import data_browser_explorer, phase_correlation_fncts
from .logger import Flags
from .custom_widgets import CustomInputForm, LoadingForm
from .res.ui_homescreen import Ui_MainWindow
from .custom_fpd_lib import fpd_processing as fpdp_new
import numpy as np
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
        self._ui.dark_mode_button.setChecked(dark_mode_config)
        self._last_path = config.get_config("file_path")
        self._files_loaded = False
        self.data_browser = None
        self.cyx = None
        self.ap = None
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
        name = self._ui.tabWidget.tabBar().tabText(idx)
        print(f"Tab {name} at {idx} has been closed")
        if name == "Data Browser":
            self.data_browser = None
        while self._ui.tabWidget.widget(idx).layout().count():
            self._ui.tabWidget.widget(idx).layout().takeAt(0).widget().deleteLater()
        self._ui.tabWidget.removeTab(idx)
        self._ui.tabWidget.setCurrentIndex(0)

    def _setup_actions(self):
        self._ui.action_mib.triggered.connect(self.function_mib)
        self._ui.action_dm3.triggered.connect(self.function_dm3)
        self._ui.action_hdf5.triggered.connect(self.function_hdf5)
        self._ui.action_npz.triggered.connect(self.function_npz)
        self._ui.actionCenter_of_Mass.triggered.connect(self.centre_of_mass)
        self._ui.actionCircular_center.triggered.connect(self.find_circular_centre)
        self._ui.actionDPC_Explorer.triggered.connect(self.start_dpc_explorer)
        self._ui.actionData_Browser.triggered.connect(self.start_dbrowser)
        self._ui.actionLoad.triggered.connect(self.load_files)
        self._ui.actionRansac_Tool.triggered.connect(self.ransac_im_fit)
        self._ui.actionVADF_Explorer.triggered.connect(self.start_vadf)
        self._ui.actionLive_Coding.triggered.connect(self.start_live_coding)

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

    @Slot()
    def change_color_mode(self):
        dark_mode_config = self._ui.dark_mode_button.isChecked()
        if self.app is not None:
            print(f"Changing theme to {dark_mode_config}")
            if dark_mode_config:
                self.app.setStyleSheet(qdarkgraystyle.load_stylesheet())
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
            print("mibline=" + str(self._ui.mib_line.text()))
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
        self.cyx = None
        self.ap = None
        for _ in range(self._ui.tabWidget.count() - 1):
            # 1 because every time a tab is removed, indices are reassigned
            self._ui.tabWidget.removeTab(1)
        if self.data_browser:
            self.data_browser = None
            self._ui.tabWidget.findChild(QMainWindow, "DataBrowserTab").deleteLater()
        logger.clear()

    @Slot()
    def load_files(self):
        """
        setp up the databrowser and open the file if not present
        """
        x_value = None
        y_value = None
        if logger.check_if_all_needed(Flags.hdf5_usage, display=False):
            logger.log("Files Loaded correctly", Flags.files_loaded)
            return
        # Cherk if Mib exist
        try:
            mib = self.mib_path
        except AttributeError:
            response = QtWidgets.QMessageBox.warning(
                self, "Warning",
                """<b>You have not provided a Merlin Binary file.</b>
                <br> Would you like to select one?""",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                valid = self.function_mib()  # load a .mib file and use it
                if not valid:  # user canceled
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
                valid = self.function_dm3()  # load a .DM3 file and use it
                if not valid:  # user canceled
                    return
                dm3 = self._dm3_path
            if response == QtWidgets.QMessageBox.No:
                logger.log("Working without a DM3 file")
                x_value = (256, 'x', 'na')
                y_value = (256, 'y', 'na')
            if response == QtWidgets.QMessageBox.Cancel:
                return

        hdr = self._mib_path[:-4] + ".hdr"
        self.mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
                               scanXalu=x_value, row_end_skip=1)

        self.ds = self.mb.get_memmap()
        x, y = self.input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                               text_y="Amount to skip for Diffraction Image")  # Check what is the maximum value
        real_skip = x
        recip_skip = y
        print("skipping : " + str(x) + " " + str(y))
        # real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        # Obvious values are 1 (no down-sample), 2, 4
        # Assign the down-sampled dataset
        self.ds_sel = self.ds[::real_skip,
                              ::real_skip, ::recip_skip, ::recip_skip]
        # remove # above to reduce total file loading - last indice is amount to skip by
        # Coordinate order is y,x,ky,kx
        # i.e. reduce real and recip space pixel count in memory

        loading_widget = LoadingForm(2, ["sum_im", "sum_dif"])
        loading_widget.setup_multi_loading("sum_im", fpdp_new.sum_im, self.ds_sel, 16, 16)
        loading_widget.setup_multi_loading("sum_dif", fpdp_new.sum_dif, self.ds_sel, 16, 16)
        loading_widget.exec()
        self.sum_dif = loading_widget.get_result("sum_dif")
        self.sum_im = loading_widget.get_result("sum_im")
        self._files_loaded = True
        logger.log("Files Loaded correctly", Flags.files_loaded)

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
        widget.exec()
        x = pow(2, widget._ui.Xsize.value())
        y = pow(2, widget._ui.Ysize.value())
        return x, y

    def closeEvent(self, event):
        config.save_config()
        event.accept()
