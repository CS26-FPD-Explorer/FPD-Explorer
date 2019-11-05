from __future__ import unicode_literals
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
from fpd.fpd_file import MerlinBinary, DataBrowser

# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_mainwindow import Ui_MainWindow
matplotlib.use('Qt5Agg')
progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.action_dm3.triggered.connect(self.function_dm3)
        self.ui.action_mib.triggered.connect(self.function_mib)
        self.last_path = "D:/Personal/PTSD/Chemestry_data"

    @Slot()
    def function_dm3(self):
        print("print from function_dm3")
        fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "Digital Micrograph files (*.dm3)")
        self.last_path = fname
        self.dm3_path = fname
        self.ui.DM3.clear()
        self.ui.DM3.insert(fname)


    @Slot()
    def function_mib(self):
        print("print from function_mib")
        fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "MERLIN binary files (*.mib)")
        self.last_path = fname
        self.mib_path = fname
        self.ui.MIB.clear()
        self.ui.MIB.insert(fname)

    @Slot()
    def LoadFiles(self):
        # QUICK FIX FOR NO DM3 SUPPLIED, MORE THOROUGH FILE CHECKING TO-DO
        try:
            dm3 = self.dm3_path
        except AttributeError:
            dm3 = []
        mib = self.mib_path
        hdr = self.mib_path[:-4]+".hdr"
        if dm3:
            # with dm3
            print("working with dm3")
            self.mb = MerlinBinary(mib, hdr, dm3, row_end_skip=1)
        else:
            # without dm3
            print("working without dm3")
            self.mb = MerlinBinary(mib, hdr, dm3, scanYalu=(256, 'y', 'na'),
                                   scanXalu=(256, 'x', 'na'), row_end_skip=1)
        
        self.ds = self.mb.get_memmap()
        real_skip = 8
        recip_skip = 8
        #real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        #Obvious values are 1 (no down-sample), 2, 4

        #Assign the down-sampled dataset
        self.ds_sel = self.ds[::real_skip,
                                ::real_skip, ::recip_skip, ::recip_skip]
        #remove # above to reduce total file loading - last indice is amount to skip by.
        #Coordinate order is y,x,ky,kx
        #i.e. reduce real and recip space pixel count in memory


        #Calulate some useful summed images for use in the DataBrowser (real space)
        # or in the VADF browser (recip space)
        self.sum_im = fpdp.sum_im(self.ds_sel, 16, 16)
        #compute summed real space image
        self.sum_dif = fpdp.sum_dif(self.ds_sel, 16, 16)

        b = DataBrowserNew(self.ds_sel, nav_im=self.sum_im,
                           fig_1=self.ui.widget_3.get_fig(),fig_2=self.ui.widget_4.get_fig())
        #QApplication.quit()
    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About")


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
