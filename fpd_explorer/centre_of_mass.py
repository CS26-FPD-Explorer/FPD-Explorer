# FPD Explorer
from . import logger
from .logger import Flags
from .custom_fpd_lib import fpd_processing as fpdp
from .custom_widgets import (
    Pop_Up_Widget,
    CustomInputRemoveAperture,
    CustomInputFormCenterOfMass,
    CustomInputFormCircularCenter,
    SingleLoadingForm
)

# NEED TO GO THROUGH PRIVATE VARIABLES


def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular centre for the users input
    parameters, when function is used it will
    bring up a figure on the UI.
    """
    if logger.check_if_all_needed(Flags.files_loaded):
        widget = CustomInputFormCircularCenter()
        widget.exec()
        canvas = Pop_Up_Widget(ApplicationWindow, "Circular Center")

        sigma = widget._ui.sigma_value.value()
        rmms_1 = widget._ui.rmms1st.value()
        rmms_2 = widget._ui.rmms2nd.value()
        rmms_3 = widget._ui.rmms3rd.value()
        ApplicationWindow._cyx, ApplicationWindow.radius = fpdp.find_circ_centre(
            ApplicationWindow._sum_dif, sigma, rmms=(rmms_1, rmms_2, rmms_3), widget=canvas)
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

        ApplicationWindow._ap = fpdp.synthetic_aperture(
            ApplicationWindow.mm_sel.shape[-2:],
            ApplicationWindow._cyx,
            rio=(0, ApplicationWindow.radius + add_radius),
            sigma=sigma, aaf=aaf)[0]
        print(ApplicationWindow._ap)
        canvas = Pop_Up_Widget(ApplicationWindow, "Aperture")
        fig = canvas.setup_docking("Aperture")
        ax = fig.get_fig().subplots()
        ax.matshow(ApplicationWindow._ap)
        logger.log("Aperture has now been correctly initialized", Flags.aperture)


def centre_of_mass(ApplicationWindow):
    """
    ADD DOCSTRING
    """
    if logger.check_if_all_needed(Flags.aperture):
        widget = CustomInputFormCenterOfMass()
        widget.exec()
        nr = widget._ui.nr.value()
        nc = widget._ui.nc.value()
        # com_yx = fpdp.center_of_mass(ApplicationWindow.mm_sel, nr, nc, thr='otsu',
        #                             aperture=ApplicationWindow._ap, parallel=False)
        loading_widget = SingleLoadingForm(ApplicationWindow.mm_sel, nr, nc, thr='otsu',
                                            aperture=ApplicationWindow._ap, parallel=False)
        loading_widget.exec()
        com_yx = loading_widget.com_yx
        # TODO: Fix the mess in another feature
        # fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
        # com_yx_cor = com_yx - fit
        # Convert to beta using the BF disc and calibration.
        # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
        # You may see that the aperture is not a perfect circle - error bars
        # cyx_sp, r_sp = fpdp.find_circ_centre(ApplicationWindow._sum_dif, sigma=2,
        #                                     rmms=(ApplicationWindow.radius-8, ApplicationWindow.radius+8, 1), spf=4)
        logger.log("Center of mass has now been found", Flags.center_mass)
        ApplicationWindow.com_yx_beta = com_yx
