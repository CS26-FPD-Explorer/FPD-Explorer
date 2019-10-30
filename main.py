from __future__ import unicode_literals
import sys
import os
os.environ["OMP_NUM_THREADS"] = "1"

import random
import matplotlib

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
        self.last_path = "d:\\"

    @Slot()
    def function_dm3(self):
        print("HELOO")
        fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "Digital Micrograph files (*.dm3)")
        self.last_path = fname
        self.dm3_path = fname
        self.ui.DM3.insert(fname)


    @Slot()
    def function_mib(self):
        print("HELOO")
        fname, fother = QFileDialog.getOpenFileName(
            self, 'Open file', self.last_path, "MERLIN binary files (*.mib)")
        self.last_path = fname
        self.mib_path = fname
        self.ui.MIB.insert(fname)

    @Slot()
    def LoadFiles(self):
        self.mb = MerlinBinary(self.mib_path, self.mib_path[:-4]+".hdr",
                               self.dm3_path, row_end_skip=1)
        self.ds = self.mb.get_memmap()
        real_skip = 4
        recip_skip = 4
        #real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
        #Obvious values are 1 (no down-sample), 2, 4

        #Assign the down-sampled dataset
        ds_sel = ds[::real_skip, ::real_skip, ::recip_skip, ::recip_skip]
        #remove # above to reduce total file loading - last indice is amount to skip by.
        #Coordinate order is y,x,ky,kx
        #i.e. reduce real and recip space pixel count in memory


        #Calulate some useful summed images for use in the DataBrowser (real space)
        # or in the VADF browser (recip space)
        sum_im = fpdp.sum_im(ds_sel, 16, 16)
        #compute summed real space image
        sum_dif = fpdp.sum_dif(ds_sel, 16, 16)


        b = DataBrowser(ds_sel, nav_im=sum_im)

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
