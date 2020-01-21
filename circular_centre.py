from PySide2 import QtWidgets

import fpd
import fpd.fpd_processing as fpdp

from custom_widgets import CustomInputFormCircularCenter

# need to go through private variables
def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular center for the current data
    """
    if ApplicationWindow._files_loaded:
        widget=CustomInputFormCircularCenter()
        widget.exec()
        sigma=widget._ui.sigma_value.value()
        rmms_1=widget._ui.rmms1st.value()
        rmms_2=widget._ui.rmms2nd.value()
        rmms_3=widget._ui.rmms3rd.value()
        ApplicationWindow.cyx,ApplicationWindow.radius = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
        sigma, rmms=(rmms_1, rmms_2, rmms_3))
    else:
        QtWidgets.QMessageBox.warning(ApplicationWindow,"Warning",
        "<b>The files must be loaded</b> before the circular center can be calculated.")
