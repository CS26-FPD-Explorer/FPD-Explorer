import sys
import os
import matplotlib
import h5py

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot

from resources.ui_mainwindow import Ui_MainWindow

from data_browser_new import DataBrowserNew
from custom_widgets import *
import data_browser_explorer

os.environ["OMP_NUM_THREADS"] = "1"

# Make sure that we are using QT5

matplotlib.use('Qt5Agg')
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
            self._update_last_path(fname)
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
                self._update_last_path(fname)
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
                self._update_last_path(fname)
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
        return data_browser_explorer.load_files(self)

    @Slot()
    def function_about(self):
        """
        Create the main windows and connect the slots
        """
        about = QtWidgets.QMessageBox()
        about.setText("<p><u>Help</u></p><p>This software allows users to process electron microscopy images, you can import 3 different types of files: .dm3,.mib and .hdf5 by Clicking  'File-&gt;Open-&gt;Filetype'.</p><p>Once the files have been loaded in, click the Pushbutton in the bottom right, the next window displayed will have defaultvalue for downsampling which is 2^3 by default, but can be modified to change the downsampling rate. After the downsampling rate has been selected, press OK and this will bring you to a window in which a selection can be made, if sum real image is selected then the real image will be shown on the left. if sum recip space is selected then an inverted image will be shown.</p><p>Once 'OK' is clicked the images will load in to the window docks and a progress bar is present to show the progress of this process. The dm3. image on the left can be navigated around byclicking on a certain pixel within the image and this will show the diffraction Image on the right at this point.</p><p><u>About</u></p><p>This software was created using QT,PySide 2, and the FPD library.</p><p>The creators are Florent Audonnet, Michal Broos, Bruce Kerr, Ruize Shen and Ewan Pandelus.</p><p> <br></p>")
        about.exec()

    def _update_last_path(self, new_path):
        self._last_path = "".join(new_path.split(".")[:-1])+"/"

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
    @Slot(int)
    def update_zoom(self, value:int):
        print(value)
    
    @Slot(str)
    def update_color_map(self, value: str):
        print(value)



fpd_app = QtWidgets.QApplication()

window = ApplicationWindow()
window.show()
sys.exit(fpd_app.exec_())
# qApp.exec_()
