import sys
import os
import matplotlib as plt
import h5py
# import qdarkgraystyle

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog, QDockWidget
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import *

from resources.ui_homescreen import Ui_MainWindow
# from resources.ui_mainwindow import Ui_MainWindow
# from resources.ui_data_browser import Ui_DataBrowser DEL

from fpd.fpd_file import MerlinBinary
from data_browser_new import DataBrowserNew
from custom_widgets import *
import data_browser_explorer, circular_centre
import config_handler as config
# from collections import OrderedDict DEL

# Make sure that we are using QT5

plt.use('Qt5Agg')
os.environ["OMP_NUM_THREADS"] = "1"


# class DataBrowserWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super(DataBrowserWidget, self).__init__()
#         self._ui = Ui_DataBrowser()
#         self._ui.setupUi(self)

#     def get_nav(self):
#         """
#         Returns the navigation widget of DataBrowser
#         """
#         return self._ui.navigationWidget

#     def get_diff(self):
#         """
#         Returns the diffraction widget of DataBrowser
#         """
#         return self._ui.diffractionWidget

class ApplicationWindow(QMainWindow):
    """
    Create the main window and connect the menu bar slots
    """

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.action_mib.triggered.connect(self.function_mib)
        self._ui.action_dm3.triggered.connect(self.function_dm3)
        # self._ui.action_hdf5.triggered.connect(self.function_hdf5)
        # self._ui.action_about.triggered.connect(self.function_about)
        # self._ui.action_Find_Circular_Center.triggered.connect(
        #     self.function_find_circular_center)

        # self._ui.darkModeButton.setChecked(dark_mode_config)

        self._data_browser = None
        self._files_loaded = False
        self._last_path = config.get_config("file_path")
        # self._init_color_map() DEL

        # makes all tabs except Home closable
        self._ui.tabWidget.tabCloseRequested.connect(self._ui.tabWidget.removeTab)
        # PySide2.QtWidgets.QTabBar.ButtonPosition for 2nd argument, LeftSide doesn't work
        self._ui.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)

    @Slot()
    def function_mib(self):
        """
        Spawn a file dialog to open an mib file
        """
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path,
            "MERLIN binary files (*.mib)")
        if fname:
            if fname[-3:] == "mib":  # empty string means user cancelled
                self._update_last_path(fname)
                self._mib_path = fname
                self._ui.mib_line.clear()
                self._ui.mib_line.insert(fname[fname.rfind('/') + 1 :])
                return True
        return False
    
    @Slot()
    def function_dm3(self):
        """
        Spawn a file dialog to open a dm3 file
        """
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path,
            "Digital Micrograph files (*.dm3)")
        if fname:
            if fname[-3:] == "dm3":
                self._update_last_path(fname)
                self._dm3_path = fname
                self._ui.dm3_line.clear()
                self._ui.dm3_line.insert(fname[fname.rfind('/') + 1 :])
                return True
        return False
    
    def _update_last_path(self, new_path):
        self._last_path = "/".join(new_path.split("/")[:-1])+"/"
        config.add_config({"file_path":self._last_path})

    @Slot()
    def load_files_new(self):
        """
        setp up the databrowser and open the file if not present
        """
        return data_browser_explorer.load_files(self)

    @Slot()
    def start_dbrowser(self):
        data_browser_explorer.start_dbrowser(self)
    
    @Slot()
    def find_circular_centre(self):
        circular_centre.find_circular_centre(self)
    # @Slot(str)
    # def update_color_map(self, value: str):
    #     data_browser_explorer.update_color_map(self, value)
    # @Slot(str)
    # def update_color_map(self, value: str):
    #     """
    #     Update the rectangle based on the value selected by the user
    #     Parameters
    #     ----------
    #     value : str name of the color map

    #     """

    #     if self._data_browser:
    #         return self._data_browser.update_color_map(value)
    #     else:
    #         self.sender().setCurrentIndex(-1)
    
    @Slot()
    def load_files(self):
        """
        setp up the databrowser and open the file if not present
        """
        x_value = None
        y_value = None
        # Cherk if Mib exist
        try:
            mib = self._mib_path
        except AttributeError:
            response = QtWidgets.QMessageBox.warning(
                self, "Warning", 
                """<strong>We noticed you don't have a Merlin Binary File</strong>
                <br> Do you want to select one ?""",
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
                """<strong>We noticed you don't have a Digital Micrograph files</strong>
                <br> Do you want to select one ?""",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Cancel:  # do nothing
                return
            elif response == QtWidgets.QMessageBox.Yes:
                valid = self.function_dm3()  # load a .DM3 file and use it
                if not valid:  # user canceled
                    return
                dm3 = self._dm3_path
            else:  # load the data using custum parameter
                # x, y = self._input_form(initial_x=8, initial_y=8, minimum=2)
                # x_value = (x, 'x', 'na')
                # y_value = (y, 'y', 'na')
                print("else")

        hdr = self._mib_path[:-4]+".hdr"
        self._mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
                                scanXalu=x_value, row_end_skip=1)

        self._ds = self._mb.get_memmap()

        x, y = self.input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                          text_y="Amount to skip for Diffraction Image")  # Check what is the maximum value
        real_skip = x
        recip_skip = y
        print("skipping : " + str(x) + " " + str(y))
        # real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        # Obvious values are 1 (no down-sample), 2, 4

        # Assign the down-sampled dataset
        self.ds_sel = self._ds[::real_skip,
                               ::real_skip, ::recip_skip, ::recip_skip]
        # remove # above to reduce total file loading - last indice is amount to skip by
        # Coordinate order is y,x,ky,kx
        # i.e. reduce real and recip space pixel count in memory

        loading_widget = CustomLoadingForm(self.ds_sel)
        loading_widget.exec()
        self._sum_dif = loading_widget._sum_dif
        self._sum_im = loading_widget._sum_im

        self._files_loaded = True
        # # Set the value to default
        # scanY, scanX = self.ds_sel.shape[:2]
        # self._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 1)
        # self._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 1)
        # self._ui.navX.setMaximum(scanX)
        # self._ui.navY.setMaximum(scanY)

        # self._sum_dif = widget.sum_dif
        # self._sum_im = widget.sum_im
        # self._data_browser = DataBrowserNew(self.ds_sel, nav_im=self._sum_im,
        #                                     widget_1=self._ui.widget_3, widget_2=self._ui.widget_4)
        print("end")
        
    def input_form(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
        """
        create an input form with the given value
        Parameters
        ----------
        initial_x int value the top value should start from
        initial_y int value the bottom value should start from
        minimum int minimum value the spin box should be allowed to go
        maximum int maximum value the spin box should be allowed to go
        text_x str Text to set in the top screen
        text_y str Text to set in the bottom screen

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


config.load_config()
fpd_app = QtWidgets.QApplication()
dark_mode_config = config.get_config("dark_mode")
if dark_mode_config:
    plt.style.use('dark_background')
    fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
window = ApplicationWindow()
window.show()
sys.exit(fpd_app.exec_())
# qApp.exec_()
