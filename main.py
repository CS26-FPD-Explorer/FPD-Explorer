import sys
import os
import matplotlib as plt
import matplotlib.pyplot as plot
import h5py
import qdarkgraystyle
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import Slot
from resources.ui_mainwindow import Ui_MainWindow

from resources.ui_inputBoxRemoveAperture import Ui_RemoveAperture



from data_browser_new import DataBrowserNew
from custom_widgets import *
import data_browser_explorer
import config_handler as config
from collections import OrderedDict

# Make sure that we are using QT5

plt.use('Qt5Agg')
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
        self._ui.action_Find_Circular_Center.triggered.connect(
            self.function_find_circular_center)
        self._ui.action_Remove_Aperture.triggered.connect(self.function_remove_aperture)
        self._ui.darkModeButton.setChecked(dark_mode_config)
        self._cyx = None
        self._data_browser = None
        self._ap = None
        self._last_path = config.get_config("file_path")
        self._init_color_map()

    @Slot()
    def function_hdf5(self):
        """
        Open an file select dialog to choose a hdf5 file 
        and open the data browser for it
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
            self._data_browser = DataBrowserNew(fname, 
            widget_1=self._ui.widget_3, widget_2=self._ui.widget_4)

    @Slot()
    def function_dm3(self):
        """
        Open an file select dialog to choose a dm3 file
        """
        print("print from function_dm3")
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path,
            "Digital Micrograph files (*.dm3)")
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
        config.add_config({"file_path":self._last_path})

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
    
    @Slot()
    def change_color_mode(self):
        dark_mode_config = self._ui.darkModeButton.isChecked()
        print(f"Changing theme to {dark_mode_config}")
        if dark_mode_config:
            fpd_app.setStyleSheet(qdarkgraystyle.load_stylesheet())
        else:
            fpd_app.setStyleSheet("")
        
        QtWidgets.QMessageBox.information(self, "Information",
        """Your settings have correctly been applied
        Note that some changes will need a restart""")
        config.add_config({"Appearence":{"dark_mode": dark_mode_config}})

    @Slot()
    def function_find_circular_center(self):
        """
        Calculate the circular center for the current data
        """
        
        
        
        
        if self._data_browser:
            widget = CustomInputFormCircularCenter()
            widget.exec()
            sigma = widget._ui.sigma_value.value()
            rmms_1 = widget._ui.rmms1st.value()
            rmms_2 = widget._ui.rmms2nd.value()
            rmms_3 = widget._ui.rmms3rd.value()
            self._cyx,self.radius = fpdp.find_circ_centre(self._sum_dif,sigma,
            rmms=(rmms_1, rmms_2, rmms_3))
            print( self._cyx)
        else:
            QtWidgets.QMessageBox.warning(self,"Warning",
            "<b>The files must be loaded</b> before the circular center can be calculated.")

    @Slot()
    def function_remove_aperture(self):
        """
        Generate aperture to limit region to BF disc. This will also allow the algorythm to go faster
        """
        err_str = ""
        
        
        if not self._data_browser:
             err_str+= "<b>The files must be loaded</b> before the aperture can be generated.<br></br><br></br>"
        
        if self._cyx is None:
             err_str += "<b>The circular center</b> must be calculated before this step can be taken. <br></br>"
        
        if err_str:
            QtWidgets.QMessageBox.warning(self,"Warning",err_str)


           
        if self._data_browser  and self._cyx.size !=0:
            widget = CustomInputRemoveAperture()
            widget.exec()
            self.sigma = widget._ui.sigma_val.value()
            add_radius = widget._ui.add_radius.value()
            self.aaf = widget._ui.aaf.value()

            self.mm_sel = self.ds_sel 
            
            
            self._ap = fpdp.synthetic_aperture(self.mm_sel.shape[-2:], self._cyx, rio = 
            (0, self.radius+add_radius), sigma=self.sigma ,aaf=self.aaf)[0]
            plot.matshow(self._ap)  
    

    def function_center_of_mass(self):
        
        err_str = ""

        if not self._data_browser:
            err_str+= "<b>The files must be loaded</b> before the center of mass can be calculated.<br></br><br></br>"

        if self._cyx is None:
            err_str += "<b>The circular center</b> must be calculated before this step can be taken.<br></br><br></br>"

        if self._ap is None:
            err_str += "<b>The aperture</b> must be generated before this step can be taken.<br></br><br></br>"
        
        if err_str:
            QtWidgets.QMessageBox.warning(self,"Warning",err_str)
 
        else: 
            widget = CustomInputFormCenterOfMass()
            widget.exec()
            nc = widget._ui.nc.value()
            nr = widget._ui.nr.value()

            com_yx = fpdp.center_of_mass(self.mm_sel, nr, nc, thr='otsu', aperture=self._ap)
            print(com_yx)
            fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
            com_yx_cor = com_yx - fit
            # Convert to beta using the BF disc and calibration.
            # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
            # You may see that the aperture is not a perfect circle - error bars

            cyx_sp, r_sp = fpdp.find_circ_centre(self._sum_dif, sigma=2, rmms=(self.radius-8, self.radius+8, 1), spf=4)
            print(r_sp)


        


       
        

    @Slot(str)
    def update_color_map(self, value: str):
        """
        Update the rectangle based on the value selected by the user
        Parameters
        ----------
        value : str name of the color map

        """

        if self._data_browser:
            return self._data_browser.update_color_map(value)
        else:
            self.sender().setCurrentIndex(-1)

    def _init_color_map(self):
        """
        Create the dictionnary to fill the color map index
        Value given by matplotlib wiki
        """
        cmaps = OrderedDict()
        cmaps['Perceptually Uniform Sequential'] = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']
        cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        cmaps['Sequential (2)'] = [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']
        cmaps['Diverging'] = [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

        cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                                'Dark2', 'Set1', 'Set2', 'Set3',
                                'tab10', 'tab20', 'tab20b', 'tab20c']
        cmaps['Miscellaneous'] = [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for el in cmaps.values():
            for cmaps in el:
                self._ui.colorMap.addItem(cmaps)

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
