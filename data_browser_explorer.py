from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QDockWidget
from PySide2.QtCore import Slot, Qt

from data_browser_new import DataBrowserNew
from collections import OrderedDict


# def load_files(ApplicationWindow):
#     """
#     setp up the databrowser and open the file if not present
#     """
#     x_value = None
#     y_value = None
#     # Cherk if Mib exist
#     try:
#         mib = ApplicationWindow._mib_path
#     except AttributeError:
#         response = QtWidgets.QMessageBox.warning(
#             ApplicationWindow, "Warning", 
#             """<strong>We noticed you don't have a Merlin Binary File</strong>
#             <br> Do you want to select one ?""",
#             QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
#             QtWidgets.QMessageBox.Yes)
#         if response == QtWidgets.QMessageBox.Yes:
#             valid = ApplicationWindow.function_mib()  # load a .mib file and use it
#             if not valid:  # user canceled
#                 return
#         else:
#             return

#     mib = ApplicationWindow._mib_path
#     # Check if dm3 exist
#     try:
#         dm3 = ApplicationWindow._dm3_path
#     except AttributeError:
#         dm3 = []
#         response = QtWidgets.QMessageBox.warning(
#             ApplicationWindow, "Warning", 
#             """<strong>We noticed you don't have a Digital Micrograph files</strong> 
#             <br> Do you want to select one ?""",
#             QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
#             QtWidgets.QMessageBox.Yes)
#         if response == QtWidgets.QMessageBox.Cancel:  # do nothing
#             return
#         elif response == QtWidgets.QMessageBox.Yes:
#             valid = ApplicationWindow.function_dm3()  # load a .DM3 file and use it
#             if not valid:  # user canceled
#                 return
#             dm3 = ApplicationWindow._dm3_path
#         else:  # load the data using custum parameter
#             x, y = input_form(initial_x=8, initial_y=8, minimum=2)
#             x_value = (x, 'x', 'na')
#             y_value = (y, 'y', 'na')

#     hdr = ApplicationWindow._mib_path[:-4]+".hdr"
#     ApplicationWindow._mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
#                             scanXalu=x_value, row_end_skip=1)

#     ApplicationWindow._ds = ApplicationWindow._mb.get_memmap()

#     x, y = input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
#                             text_y="Amount to skip for Diffraction Image")  # Check what i sthe maximum value
#     real_skip = x
#     recip_skip = y
#     print("skipping : " + str(x) + " " + str(y))
#     # real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
#     # Obvious values are 1 (no down-sample), 2, 4

#     # Assign the down-sampled dataset
#     ApplicationWindow.ds_sel = ApplicationWindow._ds[::real_skip,
#                             ::real_skip, ::recip_skip, ::recip_skip]
#     # remove # above to reduce total file loading - last indice is amount to skip by.
#     # Coordinate order is y,x,ky,kx
#     # i.e. reduce real and recip space pixel count in memory

#     widget = CustomLoadingForm(ApplicationWindow.ds_sel)
#     widget.exec()

#     # Set the value to default
#     scanY, scanX = ApplicationWindow.ds_sel.shape[:2]
#     ApplicationWindow._db_widget._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 1)
#     ApplicationWindow._db_widget._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 1)
#     ApplicationWindow._db_widget._ui.navX.setMaximum(scanX)
#     ApplicationWindow._db_widget._ui.navY.setMaximum(scanY)
    
#     ApplicationWindow._sum_dif = widget._sum_dif
#     ApplicationWindow._sum_im = widget._sum_im
 

#     ApplicationWindow._data_browser = DataBrowserNew(
#         ApplicationWindow.ds_sel, nav_im=ApplicationWindow._sum_im,
#         widget_1=ApplicationWindow._ui.navCanvas, widget_2=ApplicationWindow._ui.diffCanvas)

#     ApplicationWindow._ui.colorMap.setCurrentIndex(0)

# def input_form(initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
#     """
#     create an input form with the given value
#     Parameters
#     ----------
#     initial_x int value the top value should start from
#     initial_y int value the bottom value should start from
#     minimum int minimum value the spin box should be allowed to go
#     maximum int maximum value the spin box should be allowed to go
#     text_x str Text to set in the top screen
#     text_y str Text to set in the bottom screen

#     """

#     widget = CustomInputForm(initial_x, initial_y,
#                                 minimum, maximum, text_x, text_y)
#     widget.exec()
#     x = pow(2, widget._ui.Xsize.value())
#     y = pow(2, widget._ui.Ysize.value())
#     return x, y

from resources.ui_data_browser import Ui_DataBrowser

class DataBrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        super(DataBrowserWidget, self).__init__()
        self._ui = Ui_DataBrowser()
        self._ui.setupUi(self)

        self._data_browser = None
        self._init_color_map()

    def get_nav(self):
        """
        Returns the navigation widget of DataBrowser
        """
        return self._ui.navigationWidget

    def get_diff(self):
        """
        Returns the diffraction widget of DataBrowser
        """
        return self._ui.diffractionWidget

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
    
    @Slot(str)
    def update_color_map(self, value: str):
        """
        Update the rectangle based on the value selected by the user
        Parameters
        ----------
        value : str name of the color map

        """
        if self._data_browser:
            print("DBself="+str(self._data_browser))
            print("DBselffunction="+str(self._data_browser.update_color_map(value)))
            print("colormap value="+value)
            return self._data_browser.update_color_map(value)
        else:
            print("else="+str(self.sender().setCurrentIndex(-1)))
            self.sender().setCurrentIndex(-1)
    
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


def start_dbrowser(ApplicationWindow):
    if ApplicationWindow._files_loaded:
        w = QtWidgets.QTabBar()
        layout = QtWidgets.QHBoxLayout()
        mainwindow = QMainWindow()
        db_widget = DataBrowserWidget()

        dock = QDockWidget("Navigation", ApplicationWindow)
        dock.setWidget(db_widget.get_nav())
        mainwindow.addDockWidget(Qt.TopDockWidgetArea, dock)

        dock2 = QDockWidget("Diffraction", ApplicationWindow)
        dock2.setWidget(db_widget.get_diff())
        mainwindow.addDockWidget(Qt.TopDockWidgetArea, dock2)

        tab_index = ApplicationWindow._ui.tabWidget.addTab(mainwindow, "DataBrowser")
        ApplicationWindow._ui.tabWidget.setCurrentIndex(tab_index)

        # Set the value to default
        scanY, scanX = ApplicationWindow.ds_sel.shape[:2]
        db_widget._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 1)
        db_widget._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 1)
        db_widget._ui.navX.setMaximum(scanX)
        db_widget._ui.navY.setMaximum(scanY)
        
        print(db_widget.get_nav())
        print(db_widget.get_diff())
        ApplicationWindow._data_browser = DataBrowserNew(
            ApplicationWindow.ds_sel, nav_im=ApplicationWindow._sum_im,
            widget_1=db_widget._ui.widget_3, widget_2=db_widget._ui.widget_4)
        # navCanvas == widget_3, diffCanvas == widget_4, Flo didn't name them in data_browser.ui

        db_widget._data_browser = ApplicationWindow._data_browser
        db_widget._ui.colorMap.setCurrentIndex(0)
    else:
        QtWidgets.QMessageBox.warning(ApplicationWindow, "Warning",
        "The files must be loaded before DataBrowser can be opened.")