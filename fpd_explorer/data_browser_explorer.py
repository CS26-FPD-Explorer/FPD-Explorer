from collections import OrderedDict

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QDockWidget, QMainWindow

from .custom_fpd_lib.data_browser import DataBrowser
from .res.ui_data_browser import Ui_DataBrowser


class DataBrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        super(DataBrowserWidget, self).__init__()
        self._ui = Ui_DataBrowser()
        self._ui.setupUi(self)

        self._data_browser = None
        self._init_color_map()

    def setup_ui(self, shape: tuple):
        """
        Setup of all the default value for the explorer
        """
        # Set the value to default
        scanY, scanX = shape
        self._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 1)
        self._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 1)
        self._ui.navX.setMaximum(scanX)
        self._ui.navY.setMaximum(scanY)
        self._ui.colorMap.setCurrentIndex(0)

    def set_data_browser(self, data_browser):
        """
        Secure setter for the databrowser variable
        """
        self._data_browser = data_browser
        print(self._data_browser)

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

        ApplicationWindow._data_browser = DataBrowser(
            ApplicationWindow.ds_sel, nav_im=ApplicationWindow._sum_im,
            widget_1=db_widget._ui.navCanvas, widget_2=db_widget._ui.diffCanvas)
        # navCanvas == widget_3, diffCanvas == widget_4, Flo didn't name them in data_browser.ui

        db_widget.set_data_browser(ApplicationWindow._data_browser)
        db_widget.setup_ui(ApplicationWindow.ds_sel.shape[:2])
    else:
        QtWidgets.QMessageBox.warning(ApplicationWindow, "Warning",
                                      "<b>The files must be loaded</b> before DataBrowser can be opened.")
