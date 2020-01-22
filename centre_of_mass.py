import matplotlib.pyplot as plot

from PySide2 import QtWidgets

import fpd
import fpd.fpd_processing as fpdp

from custom_widgets import CustomInputFormCircularCenter, CustomInputRemoveAperture, CustomInputFormCenterOfMass

# NEED TO GO THROUGH PRIVATE VARIABLES
def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular centre for the current data
    """
    if ApplicationWindow._files_loaded:
        widget=CustomInputFormCircularCenter()
        widget.exec()
        sigma=widget._ui.sigma_value.value()
        rmms_1=widget._ui.rmms1st.value()
        rmms_2=widget._ui.rmms2nd.value()
        rmms_3=widget._ui.rmms3rd.value()
        ApplicationWindow._cyx,ApplicationWindow.radius = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
        sigma, rmms=(rmms_1, rmms_2, rmms_3))
    else:
        QtWidgets.QMessageBox.warning(ApplicationWindow,"Warning",
        "<b>The files must be loaded</b> before the circular centre can be calculated.")

def remove_aperture(ApplicationWindow):
    """
    Generate aperture to limit region to BF disc. This will also allow the algorithm to go faster
    """
    err_str = ""
    
    if not ApplicationWindow._files_loaded:
        err_str += "<b>The files must be loaded</b> before the aperture can be generated.<br><br>"
    
    if ApplicationWindow._cyx is None:
        err_str += "<b>The circular centre must be calculated</b> before this step can be taken."
    
    if err_str:
        QtWidgets.QMessageBox.warning(ApplicationWindow,"Warning",err_str)
        return

    if ApplicationWindow._files_loaded and ApplicationWindow._cyx.size != 0:
        widget = CustomInputRemoveAperture()
        widget.exec()
        sigma = widget._ui.sigma_val.value()
        add_radius = widget._ui.add_radius.value()
        aaf = widget._ui.aaf.value()

        ApplicationWindow.mm_sel = ApplicationWindow.ds_sel 
        
        ApplicationWindow._ap = fpdp.synthetic_aperture(ApplicationWindow.mm_sel.shape[-2:],
        ApplicationWindow._cyx, rio = (0, ApplicationWindow.radius+add_radius), sigma=sigma, aaf=aaf)[0]
        plot.matshow(ApplicationWindow._ap)  

def centre_of_mass(ApplicationWindow):
    """
    ADD DOCSTRING
    """
    err_str = ""

    if not ApplicationWindow._files_loaded:
        err_str += "<b>The files must be loaded</b> before the centre of mass can be calculated.<br><br>"

    if ApplicationWindow._cyx is None:
        err_str += "<b>The circular centre must be calculated</b> before this step can be taken.<br><br>"

    if ApplicationWindow._ap is None:
        err_str += "<b>The aperture must be generated</b> before this step can be taken."
    
    if err_str:
        QtWidgets.QMessageBox.warning(ApplicationWindow,"Warning",err_str)
    else: 
        widget = CustomInputFormCenterOfMass()
        widget.exec()
        nr = widget._ui.nr.value()
        nc = widget._ui.nc.value()

        com_yx = fpdp.center_of_mass(ApplicationWindow.mm_sel, nr, nc, thr='otsu', aperture=ApplicationWindow._ap)
        
        fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
        com_yx_cor = com_yx - fit
        # Convert to beta using the BF disc and calibration.
        # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
        # You may see that the aperture is not a perfect circle - error bars
        cyx_sp, r_sp = fpdp.find_circ_centre(ApplicationWindow._sum_dif, sigma=2,
                        rmms=(ApplicationWindow.radius-8, ApplicationWindow.radius+8, 1), spf=4)
