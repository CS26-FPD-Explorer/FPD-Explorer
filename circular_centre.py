from PySide2 import QtWidgets
# from PySide2.QtWidgets import QMainWindow, QDockWidget
# from PySide2.QtCore import Slot, Qt

# from data_browser_new import DataBrowserNew
# from collections import OrderedDict
# from resources.ui_data_browser import Ui_DataBrowser
import fpd
import fpd.fpd_processing as fpdp
# import fpd_processing_new as fpdp_new
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
