import sys
import os
import matplotlib
import h5py

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot

from resources.ui_homescreen import Ui_MainWindow
# from resources.ui_mainwindow import Ui_MainWindow

from data_browser_new import DataBrowserNew
from custom_widgets import *
import data_browser_explorer
from collections import OrderedDict

os.environ["OMP_NUM_THREADS"] = "1"

# Make sure that we are using QT5

matplotlib.use('Qt5Agg')
os.environ["OMP_NUM_THREADS"] = "1"


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

        self._data_browser = None
        self._last_path = ""

    @Slot()
    def function_mib(self):
        """
        Spawn a file dialog to open an mib file
        """
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path, "MERLIN binary files (*.mib)")
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
            self, 'Open file', self._last_path, "Digital Micrograph files (*.dm3)")
        if fname:
            if fname[-3:] == "dm3":
                self._update_last_path(fname)
                self._dm3_path = fname
                self._ui.dm3_line.clear()
                self._ui.dm3_line.insert(fname[fname.rfind('/') + 1 :])
                return True
        return False
    
    def _update_last_path(self, new_path):
        self._last_path = "".join(new_path.split(".")[:-1])+"/"

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
                self, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
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
                self, "Warning", "<strong>We noticed you don't have a Digital Micrograph files</strong> <br> Do you want to select one ?",
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

        x, y = self._input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                                text_y="Amount to skip for Diffraction Image")  # Check what i sthe maximum value
        real_skip = x
        recip_skip = y
        print("skipping : " + str(x) + " " + str(y))
        # real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        # Obvious values are 1 (no down-sample), 2, 4

        # Assign the down-sampled dataset
        self.ds_sel = self._ds[::real_skip,
                               ::real_skip, ::recip_skip, ::recip_skip]
        # remove # above to reduce total file loading - last indice is amount to skip by.
        # Coordinate order is y,x,ky,kx
        # i.e. reduce real and recip space pixel count in memory

        widget = CustomLoadingForm(self.ds_sel)
        widget.exec()

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
        
    def _input_form(self, initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
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

        widget = CustomInputForm(initial_x, initial_y, minimum, maximum, text_x, text_y)
        widget.exec()
        x = pow(2, widget._ui.Xsize.value())
        y = pow(2, widget._ui.Ysize.value())
        return x, y




    # @Slot()
    # def LoadFiles(self):
    #     x_value = None
    #     y_value = None
    #     #Cherk if Mib exist
    #     try:
    #         mib = self.mib_path
    #     except AttributeError:
    #         response = QtWidgets.QMessageBox.warning(
    #             self, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
    #             QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #             QtWidgets.QMessageBox.Yes)
    #         if response == QtWidgets.QMessageBox.Yes:
    #             valid = self.function_mib()  # load a .mib file and use it
    #             if not valid: #user canceled
    #                 return 
    #         else:
    #             return


fpd_app = QtWidgets.QApplication()

window = ApplicationWindow()
# window.setWindowTitle("%s" % progname)
window.show()
sys.exit(fpd_app.exec_())
# qApp.exec_()
