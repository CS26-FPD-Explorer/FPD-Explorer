import os
import sys

from fpd.fpd_file import MerlinBinary
from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QFileDialog, QMainWindow

import qdarkgraystyle

from . import centre_of_mass
from . import config_handler as config
from . import data_browser_explorer
from .custom_widgets import *
from .res.ui_homescreen import Ui_MainWindow


class ApplicationWindow(QMainWindow):
    """
    Create the main window and connect the menu bar slots
    """

    def __init__(self, app=None, dark_mode_config=False):
        super(ApplicationWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.app = app
        self.dark_mode_config = dark_mode_config

        self._ui.action_mib.triggered.connect(self.function_mib)
        self._ui.action_dm3.triggered.connect(self.function_dm3)
        # self._ui.action_hdf5.triggered.connect(self.function_hdf5)
        self._ui.action_about.triggered.connect(self.function_about)

        self._ui.dark_mode_button.setChecked(dark_mode_config)
        self._last_path = config.get_config("file_path")

        self._files_loaded = False
        self._data_browser = None
        self._cyx = None
        self._ap = None

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
                self._ui.mib_line.insert(fname[fname.rfind('/') + 1:])
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
                self._ui.dm3_line.insert(fname[fname.rfind('/') + 1:])
                return True
        return False

    @Slot()
    def function_about(self):
        """
        Display a pop-up describing the software.
        """
        about = QtWidgets.QMessageBox()
        about.setText("""<p><u>Help</u></p><p>This software allows users to process electron 
        microscopy images, you can import 3 different types of files: .dm3,.mib and .hdf5 by Clicking 
         'File-&gt;Open-&gt;Filetype'.</p><p>Once the files have been loaded in, click the Pushbutton 
         in the bottom right, the next window displayed will have defaultvalue for downsampling which 
         is 2^3 by default, but can be modified to change the downsampling rate. After the 
         downsampling rate has been selected, press OK and this will bring you to a window in which a 
         selection can be made, if sum real image is selected then the real image will be shown on 
         the left. if sum recip space is selected then an inverted image will be shown.</p><p>Once 
         'OK' is clicked the images will load in to the window docks and a progress bar is present to 
         show the progress of this process. The dm3. image on the left can be navigated around 
         byclicking on a certain pixel within the image and this will show the diffraction Image on 
         the right at this point.</p><p><u>About</u></p><p>This software was created using QT,PySide 
         2, and the FPD library.</p><p>The creators are Florent Audonnet, Michal Broos, Bruce Kerr, 
         Ruize Shen and Ewan Pandelus.</p><p> <br></p>""")
        about.exec()

    def _update_last_path(self, new_path):
        self._last_path = "/".join(new_path.split("/")[:-1])+"/"
        config.add_config({"file_path": self._last_path})

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
    def start_dbrowser(self):
        data_browser_explorer.start_dbrowser(self)

    @Slot()
    def find_circular_centre(self):
        centre_of_mass.find_circular_centre(self)

    @Slot()
    def remove_aperture(self):
        centre_of_mass.remove_aperture(self)

    @Slot()
    def centre_of_mass(self):
        centre_of_mass.centre_of_mass(self)

    @Slot()
    def clear_files(self):
        """
        Clears all provided files and resets the file_loaded flag
        """
        if self._ui.mib_line.text():
            print("mibline="+str(self._ui.mib_line.text()))
            del self._mib_path
            self._ui.mib_line.clear()
        if self._ui.dm3_line.text():
            del self._dm3_path
            self._ui.dm3_line.clear()
        if self._ui.hdf5_line.text():
            # TO DO: ADD hdf5 RELEVANT CODE ONCE hdf5 OPENING ADDED
            pass
        self._files_loaded = False
        self._cyx = None
        self._ap = None

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
            else:  # load the data using custum parameter
                return

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
        print("files_loaded="+str(self._files_loaded))
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
