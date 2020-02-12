import fpd
from .custom_fpd_lib import fpd_processing as fpdp
from .custom_widgets import MyMplCanvas
import matplotlib.pyplot as plot
from PySide2 import QtWidgets


from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QDockWidget, QMainWindow, QGridLayout, QPushButton, QHBoxLayout

from .custom_widgets import (CustomInputFormCenterOfMass,
                             CustomInputFormCircularCenter,
                             CustomInputRemoveAperture,
                             )
from .res.ui_popUpCanvas import Ui_PopUpCanvas

from . import logger
from .logger import Flags


class Pop_Up_Widget(QtWidgets.QWidget):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered
    mainwindow : QMainWindow The main window in which the dock widget should get created

    """

    def __init__(self, ApplicationWindow):
        super(Pop_Up_Widget, self).__init__()
        self._ui = Ui_PopUpCanvas()
        self._ui.setupUi(self)
        self.application_window = ApplicationWindow
        self.main_window = QMainWindow()

    def setup_docking(self, name):
        """
        Initialize a dock widget with the given name
        Parameters
        ----------
        name : str the name of the dock widget window

        Return
        ---------
        widget : QWidget the widget inside of the dock widget or None if no widget available
        location : tuple Position where we want the docking to be
        """
        widget = self

        self.dock = QDockWidget(name, self.application_window)
        self.dock.setWidget(widget)
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea
                                  | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        loc = Qt.TopDockWidgetArea
        self.main_window.addDockWidget(loc, self.dock)
        self.tab_index = self.application_window._ui.tabWidget.addTab(self.main_window, name)
        self.application_window._ui.tabWidget.setCurrentIndex(self.tab_index)

        return self._ui.canvas

    @Slot()
    def accept(self):
        self.dock.close()
        self.application_window._ui.tabWidget.removeTab(self.tab_index)


# NEED TO GO THROUGH PRIVATE VARIABLES
def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular centre for the users input 
    parameters, when function is used it will 
    bring up a figure on the UI.
    """
    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow)
        fig = canvas.setup_docking("Circular Centre")

        widget = CustomInputFormCircularCenter()
        widget.exec()
        sigma = widget._ui.sigma_value.value()
        rmms_1 = widget._ui.rmms1st.value()
        rmms_2 = widget._ui.rmms2nd.value()
        rmms_3 = widget._ui.rmms3rd.value()
        ApplicationWindow._cyx, ApplicationWindow.radius = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
                                                                                 sigma, rmms=(rmms_1, rmms_2, rmms_3), widget=fig)
        logger.log("Circular center has now been initialized", Flags.circular_center)


def remove_aperture(ApplicationWindow):
    """
    Generates a synthetic aperture for the users input 
    parameters, when function is used it will 
    bring up a figure on the UI.
    """

    if logger.check_if_all_needed(Flags.circular_center):
        widget = CustomInputRemoveAperture()
        widget.exec()
        sigma = widget._ui.sigma_val.value()
        add_radius = widget._ui.add_radius.value()
        aaf = widget._ui.aaf.value()

        ApplicationWindow.mm_sel = ApplicationWindow.ds_sel

        ApplicationWindow._ap = fpdp.synthetic_aperture(ApplicationWindow.mm_sel.shape[-2:],
                                                        ApplicationWindow._cyx, rio=(0, ApplicationWindow.radius+add_radius), sigma=sigma, aaf=aaf)[0]
        print(ApplicationWindow._ap)
        canvas = Pop_Up_Widget(ApplicationWindow)
        fig = canvas.setup_docking("Circular Centre")
        ax = fig.get_fig().subplots()
        ax.matshow(ApplicationWindow._ap)
        logger.log("Aperture has now been correctly initialized", Flags.aperture)


def centre_of_mass(ApplicationWindow):
    """
    ADD DOCSTRING
    """
    err_str = ""
    if logger.check_if_all_needed(Flags.aperture):
        widget = CustomInputFormCenterOfMass()
        widget.exec()
        nr = widget._ui.nr.value()
        nc = widget._ui.nc.value()
        com_yx = fpdp.center_of_mass(ApplicationWindow.mm_sel, nr, nc, thr='otsu',
                                     aperture=ApplicationWindow._ap, parallel=False)

        fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
        com_yx_cor = com_yx - fit
        # Convert to beta using the BF disc and calibration.
        # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
        # You may see that the aperture is not a perfect circle - error bars
        cyx_sp, r_sp = fpdp.find_circ_centre(ApplicationWindow._sum_dif, sigma=2,
                                             rmms=(ApplicationWindow.radius-8, ApplicationWindow.radius+8, 1), spf=4)
        logger.log("Center of mass has now been found", Flags.center_mass)
