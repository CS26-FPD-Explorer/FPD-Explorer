from PySide2 import QtWidgets
from PySide2.QtCore import Slot

# FPD Explorer
from . import logger
from .logger import Flags
from .custom_widgets import Pop_Up_Widget
from .res.ui_data_browser import Ui_DataBrowser
from .custom_fpd_lib.data_browser import DataBrowser


class DataBrowserWidget(QtWidgets.QWidget):
    """
    Initialize the required widget needed by Data Browser tab
    """

    def __init__(self, ApplicationWindow):
        super(DataBrowserWidget, self).__init__()
        self._ui = Ui_DataBrowser()
        self._ui.setupUi(self)
        self.application_window = ApplicationWindow
        self.data_browser = None
        self._init_color_map()

    def setup_ui(self, shape: tuple):
        """
        Setup of all default values for the DataBrowser
        """
        # Set the value to default
        scanY, scanX = shape
        self._ui.navX.setValue(scanX // 64 if scanX // 64 != 0 else 1)
        self._ui.navY.setValue(scanY // 64 if scanY // 64 != 0 else 1)
        self._ui.navX.setMaximum(scanX)
        self._ui.navY.setMaximum(scanY)
        self._ui.colorMap.setCurrentIndex(0)

    def set_data_browser(self, data_browser):
        """
        Secure setter for the databrowser variable
        """
        self.data_browser = data_browser

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
        Values given by matplotlib wiki
        """

        for el in self.application_window.cmaps.values():
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
        if self.data_browser:
            return self.data_browser.update_color_map(value)
        else:
            self.sender().setCurrentIndex(0)

    @Slot()
    def recenter_dif_plot(self):
        return self.data_browser.recenter_dif_plot()

    @Slot(int)
    def update_rect(self, value: int):
        """
        Update the rectangle based on the value selected by the SpinBox
        Parameters
        ----------
        value : int new value to set the rectangle to

        """
        if self.data_browser:
            return self.data_browser.update_rect(value, self.sender().objectName())
        else:
            self.sender().setValue(1)


def start_dbrowser(ApplicationWindow):
    """
    Start the data browser and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """
    if ApplicationWindow.data_browser:
        ApplicationWindow._ui.tabWidget.setCurrentWidget(
            ApplicationWindow._ui.tabWidget.findChild(QtWidgets.QWidget, "Data Browser"))
        return
    if logger.check_if_all_needed(Flags.files_loaded):
        ApplicationWindow.db_widget = DataBrowserWidget(ApplicationWindow)
        db_tab = Pop_Up_Widget(ApplicationWindow, "Data Browser")
        db_tab.setup_docking_default(ApplicationWindow.db_widget.get_nav())
        db_tab.setup_docking_default(ApplicationWindow.db_widget.get_diff())
        hdf5_usage = logger.check_if_all_needed(Flags.hdf5_usage, display=False)
        if hdf5_usage:
            ApplicationWindow.db_widget.setup_ui(ApplicationWindow.ds.shape[:2])
            ApplicationWindow.data_browser = DataBrowser(
                ApplicationWindow.hdf5_path,
                widget_1=ApplicationWindow.db_widget._ui.navCanvas,
                widget_2=ApplicationWindow.db_widget._ui.diffCanvas)

        else:
            ApplicationWindow.db_widget.setup_ui(ApplicationWindow.ds_sel.shape[:2])
            ApplicationWindow.data_browser = DataBrowser(
                ApplicationWindow.ds_sel,
                nav_im=ApplicationWindow.sum_im,
                widget_1=ApplicationWindow.db_widget._ui.navCanvas,
                widget_2=ApplicationWindow.db_widget._ui.diffCanvas)

        ApplicationWindow.db_widget.set_data_browser(ApplicationWindow.data_browser)
        logger.log("Data Browser has been opened")
