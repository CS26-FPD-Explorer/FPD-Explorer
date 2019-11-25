from __future__ import unicode_literals
import sys
import os
import matplotlib
import random
import numpy as np
import scipy as sp
import h5py

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot

from fpd.fpd_file import MerlinBinary

from ui_inputbox import Ui_InputBox
from ui_mainwindow import Ui_MainWindow
from DataBrowserNew import DataBrowserNew
from custom_widgets import *

os.environ["OMP_NUM_THREADS"] = "1"

# Make sure that we are using QT5

# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets
matplotlib.use('Qt5Agg')
progname = os.path.basename(sys.argv[0])
progversion = "0.1"
os.environ["OMP_NUM_THREADS"] = "1"


class ApplicationWindow(QMainWindow):
    """
    Create the main windows and connect the slots
    """

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.action_dm3.triggered.connect(self.function_dm3)
        self._ui.action_mib.triggered.connect(self.function_mib)
        self._ui.action_hdf5.triggered.connect(self.function_hdf5)
        self._ui.action_about.triggered.connect(self.function_about)

        self._data_browser = None
        self._last_path = "D:/Personal/PTSD/Chemestry_data"

    @Slot()
    def function_hdf5(self):
        """
        Open an file select dialog to choose a hdf5 file and open the data browser for it
        """
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path, "HDF5 (*.hdf5)")
        if fname:
            self._last_path = fname
            # ask whats the point of doing that
            self._file = h5py.File(fname, 'r')
            self._ds = self._file['fpd_expt/fpd_data/data']
            self._sum_im = self._file['fpd_expt/fpd_sum_im/data'].value
            self._sum_dif = self._file['fpd_expt/fpd_sum_dif/data'].value
            # since it is never used
            self._data_browser = DataBrowserNew(fname, widget_1=self._ui.widget_3,
                                                widget_2=self._ui.widget_4)

    @Slot()
    def function_dm3(self):
        """
        Open an file select dialog to choose a dm3 file
        """

        print("print from function_dm3")
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path, "Digital Micrograph files (*.dm3)")
        if fname:
            if fname[-3:] == "dm3":
                self._last_path = fname
                self._dm3_path = fname
                self._ui.DM3.clear()
                self._ui.DM3.insert(fname)
                return True
        return False

    @Slot()
    def function_mib(self):
        """
        Open an file select dialog to choose a mib file
        """
        print("print from function_mib")
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path, "MERLIN binary files (*.mib)")
        if fname:
            if fname[-3:] == "mib":  # empty string means user canceled
                self._last_path = fname
                self._mib_path = fname
                self._ui.MIB.clear()
                self._ui.MIB.insert(fname)
                return True
        return False

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
                x, y = self._input_form(initial_x=8, initial_y=8, minimum=2)
                x_value = (x, 'x', 'na')
                y_value = (y, 'y', 'na')

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
        # Set the value to default
        scanY, scanX = self.ds_sel.shape[:2]
        self._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 2)
        self._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 2)
        self._ui.navX.setMaximum(scanX)
        self._ui.navY.setMaximum(scanY)

        self._sum_dif = widget.sum_dif
        self._sum_im = widget.sum_im
        self._data_browser = DataBrowserNew(self.ds_sel, nav_im=self._sum_im,
                                            widget_1=self._ui.widget_3, widget_2=self._ui.widget_4)

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

        widget = CustomInputForm(initial_x, initial_y,
                                 minimum, maximum, text_x, text_y)
        widget.exec()
        x = pow(2, widget._ui.Xsize.value())
        y = pow(2, widget._ui.Ysize.value())
        return x, y

    @Slot()
    def function_about(self):
        """
        Create the main windows and connect the slots
        """
        about = QtWidgets.QMessageBox()
        about.setText("<p><u>Help</u></p><p>This software allows users to process electron microscopy images, you can import 3 different types of files: .dm3,.mib and .hdf5 by Clicking  'File-&gt;Open-&gt;Filetype'.</p><p>Once the files have been loaded in, click the Pushbutton in the bottom right, the next window displayed will have defaultvalue for downsampling which is 2^3 by default, but can be modified to change the downsampling rate. After the downsampling rate has been selected, press OK and this will bring you to a window in which a selection can be made, if sum real image is selected then the real image will be shown on the left. if sum recip space is selected then an inverted image will be shown.</p><p>Once 'OK' is clicked the images will load in to the window docks and a progress bar is present to show the progress of this process. The dm3. image on the left can be navigated around byclicking on a certain pixel within the image and this will show the diffraction Image on the right at this point.</p><p><u>About</u></p><p>This software was created using QT,PySide 2, and the FPD library.</p><p>The creators are Florent Audonnet, Michal Broos, Bruce Kerr, Ruize Shen and Ewan Pandelus.</p><p> <br></p>")
        about.exec()

    @Slot(int)
    def update_rect(self, value: int):
        """
        Update the rectangle based on the value selected by the SpinBox
        Parameters
        ----------
        value : int new value to set the rectangle to

        """

        if self._data_browser:
            return self._data_browser.update_rect(value, self.sender().objectName())
        else:
            self.sender().setValue(1)


fpd_app = QtWidgets.QApplication()

window = ApplicationWindow()
window.setWindowTitle("%s" % progname)
window.show()
sys.exit(fpd_app.exec_())
# qApp.exec_()
