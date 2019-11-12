from __future__ import unicode_literals
from custom_widgets import *
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from ui_inputbox import Ui_InputBox
from fpd.fpd_file import MerlinBinary
import h5py
import sys
import os
os.environ["OMP_NUM_THREADS"] = "1"

import random
import matplotlib
from DataBrowserNew import DataBrowserNew
import scipy as sp
import numpy as np
# Make sure that we are using QT5
import fpd
import fpd.fpd_processing as fpdp
import fpd.fpd_file as fpdf
from fpd.ransac_tools import ransac_1D_fit, ransac_im_fit

# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
matplotlib.use('Qt5Agg')
progname = os.path.basename(sys.argv[0])
progversion = "0.1"
os.environ["OMP_NUM_THREADS"] = "1"


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_dm3.triggered.connect(self.function_dm3)
        self.ui.action_mib.triggered.connect(self.function_mib)
        self.ui.action_hdf5.triggered.connect(self.function_hdf5)
        self.ui.action_about.triggered.connect(self.function_about)

        self.last_path = "D:/Personal/PTSD/Chemestry_data"

    @Slot()
    def function_hdf5(self):
        fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "HDF5 (*.hdf5)")
        if fname:
            self.last_path = fname
            #ask whats the point of doing that 
            self.f = h5py.File(fname, 'r')
            self.ds = self.f['fpd_expt/fpd_data/data']
            self.sum_im = self.f['fpd_expt/fpd_sum_im/data'].value
            self.sum_dif = self.f['fpd_expt/fpd_sum_dif/data'].value
            # since it is never used
            b = DataBrowserNew(fname, widget_1=self.ui.widget_3,
                            widget_2=self.ui.widget_4)



    @Slot()
    def function_dm3(self):
        print("print from function_dm3")
        while True:
            fname, fother = QFileDialog.getOpenFileName(
                self, 'Open file', self.last_path, "Digital Micrograph files (*.dm3)")
            if fname:
                if fname[slice(-3, None)] == "dm3":
                    self.last_path = fname
                    self.dm3_path = fname
                    self.ui.DM3.clear()
                    self.ui.DM3.insert(fname)
                    break


    @Slot()
    def function_mib(self):
        print("print from function_mib")
        while True:
            fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "MERLIN binary files (*.mib)")
            if fname and fname[slice(-3, None)] == "mib":
                self.last_path = fname
                self.mib_path = fname
                self.ui.MIB.clear()
                self.ui.MIB.insert(fname)
                break

    @Slot()
    def LoadFiles(self):
        # QUICK FIX FOR NO DM3 SUPPLIED, MORE THOROUGH FILE CHECKING TO-DO
        x_value = None
        y_value = None
        #Cherk if Mib exist
        try:
            mib = self.mib_path
        except AttributeError:
            response = QtWidgets.QMessageBox.warning(
                self, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                self.function_mib()  # load a .DM3 file and use it
            else:
                return

        mib = self.mib_path
        #Check if dm3 exist
        try:
            dm3 = self.dm3_path
        except AttributeError:
            dm3 = []
            response = QtWidgets.QMessageBox.warning(
                self, "Warning", "<strong>We noticed you don't have a Digital Micrograph files</strong> <br> Do you want to select one ?",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Cancel:#do nothing
                return
            elif response == QtWidgets.QMessageBox.Yes:
                self.function_dm3()  # load a .DM3 file and use it
                dm3 = self.dm3_path
            else:  # load the data using custum parameter
                x, y = self.input_form(initial_x = 8, initial_y = 8, minimum = 2)
                x_value = (x, 'x', 'na')
                y_value = (y, 'y', 'na')



        hdr = self.mib_path[:-4]+".hdr"
        self.mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
                                   scanXalu=x_value, row_end_skip=1)
        
        self.ds = self.mb.get_memmap()


        x, y = self.input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                               text_y="Amount to skip for Diffraction Image")  # Check what i sthe maximum value
        real_skip = x
        recip_skip = y
        print("skipping : " + str(x) + " "+  str(y))
        #real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        #Obvious values are 1 (no down-sample), 2, 4

        #Assign the down-sampled dataset
        self.ds_sel = self.ds[::real_skip,
                                ::real_skip, ::recip_skip, ::recip_skip]
        #remove # above to reduce total file loading - last indice is amount to skip by.
        #Coordinate order is y,x,ky,kx
        #i.e. reduce real and recip space pixel count in memory

        widget = CustomLoadingForm()
        widget.set_ds_sel(self.ds_sel)
        widget.exec()
        b = DataBrowserNew(self.ds_sel, nav_im=widget.sum_im,
                           widget_1=self.ui.widget_3, widget_2=self.ui.widget_4)

    def input_form(self, initial_x = 2, initial_y = 2, minimum = 0, maximum = 13, text_x = None, text_y = None):
        widget = CustomInputForm(initial_x, initial_y, minimum, maximum, text_x, text_y)
        widget.exec()
        x = pow(2,widget.ui.Xsize.value())
        y = pow(2, widget.ui.Ysize.value())
        return x,y

    def function_about(self):
        self.about = QtWidgets.QMessageBox()
        self.about.setText("<p><u>Help</u></p><p>This software allows users to process electron microscopy images, you can import 3 different types of files: .dm3,.mib and .hdf5 by Clicking 'File-&gt;Open-&gt;Filetype'.</p><p>Once the files have been loaded in, click the Pushbutton in the bottom right, the next window displayed will have defaultvalue for downsampling which is 2^3 by default, but can be modified to change the downsampling rate. After the downsampling rate has been selected, press OK and this will bring you to a window in which a selection can be made, if sum real image is selected then the real image will be shown on the left. if sum recip space is selected then an inverted image will be shown.</p><p>Once 'OK' is clicked the images will load in to the window docks and a progress bar is present to show the progress of this process. The dm3. image on the left can be navigated around byclicking on a certain pixel within the image and this will show the diffraction Image on the right at this point.</p><p><u>About</u></p><p>This software was created using QT,PySide 2, and the FPD library.</p><p>The creators are Florent Audonnet, Michal Broos, Bruce Kerr, Ruize Shen and Ewan Pandelus.</p><p> <br></p>")
        self.about.exec()

qApp = QtWidgets.QApplication()

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
