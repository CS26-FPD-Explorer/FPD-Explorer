from PySide2 import QtWidgets

import fpd
import fpd.fpd_processing as fpdp

from custom_widgets import CustomInputFormCircularCenter

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
        print(sigma,rmms_1,rmms_2,rmms_3)
        ##lowest_input_radius,max_radius,number_of_circles
        ApplicationWindow.cyx,ApplicationWindow.radius = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
        sigma, rmms=(rmms_1, rmms_2, rmms_3))
        print("desired code reached")
    else:
        QtWidgets.QMessageBox.warning(ApplicationWindow,"Warning",
        "The files must be loaded before the circular center can be calculated.")
