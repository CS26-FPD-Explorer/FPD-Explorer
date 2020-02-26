from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QDockWidget, QMainWindow

# FPD Explorer
from . import logger
from .logger import Flags
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
        self._data_browser = None
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
        self._data_browser = data_browser
        print("Data browser set up")

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
        if self._data_browser:
            return self._data_browser.update_color_map(value)
        else:
            print("else=" + str(self.sender()))
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

    def close_handler(self):
        try:
            self.get_nav().parentWidget().close()
            self.get_diff().parentWidget().close()
        except:
            pass
        self.application_window._data_browser = None
        self.application_window._ui.tabWidget.findChild(QMainWindow, "DataBrowserTab").deleteLater()


def start_dbrowser(ApplicationWindow):
    """
    Start the data browser and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """
    if ApplicationWindow._data_browser:
        ApplicationWindow._ui.tabWidget.setCurrentWidget(
            ApplicationWindow._ui.tabWidget.findChild(QMainWindow, "DataBrowserTab"))
        return
    if logger.check_if_all_needed(Flags.files_loaded):
        mainwindow = QMainWindow()
        mainwindow.setObjectName("DataBrowserTab")
        db_widget = DataBrowserWidget(ApplicationWindow)

        dock = QDockWidget("Navigation", ApplicationWindow)
        dock.setWidget(db_widget.get_nav())
        mainwindow.addDockWidget(Qt.TopDockWidgetArea, dock)

        dock2 = QDockWidget("Diffraction", ApplicationWindow)
        dock2.setWidget(db_widget.get_diff())
        mainwindow.addDockWidget(Qt.TopDockWidgetArea, dock2)

        tab_index = ApplicationWindow._ui.tabWidget.addTab(mainwindow, "DataBrowser")
        ApplicationWindow._ui.tabWidget.setCurrentIndex(tab_index)
        ApplicationWindow._ui.tabWidget.setTabToolTip(tab_index, ApplicationWindow._ui.mib_line.text())
        hdf5_usage = logger.check_if_all_needed(Flags.hdf5_usage, display=False)
        if hdf5_usage:
            ApplicationWindow._data_browser = DataBrowser(
                ApplicationWindow.hdf5_path, widget_1=db_widget._ui.navCanvas, widget_2=db_widget._ui.diffCanvas)

        else:
            ApplicationWindow._data_browser = DataBrowser(
                ApplicationWindow.ds_sel, nav_im=ApplicationWindow._sum_im,
                widget_1=db_widget._ui.navCanvas, widget_2=db_widget._ui.diffCanvas)

        ApplicationWindow._ui.tabWidget.tabCloseRequested.connect(db_widget.close_handler)
        db_widget.set_data_browser(ApplicationWindow._data_browser)
        if hdf5_usage:
            db_widget.setup_ui(ApplicationWindow._ds.shape[:2])
        else:
            db_widget.setup_ui(ApplicationWindow.ds_sel.shape[:2])

        logger.log("Data Browser has been opened")
