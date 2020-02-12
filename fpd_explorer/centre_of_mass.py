import fpd
import matplotlib.pyplot as plot
import fpd.fpd_processing as fpdp

# FPD Explorer
from . import logger
from .logger import Flags
from .custom_widgets import CustomInputRemoveAperture, CustomInputFormCenterOfMass, CustomInputFormCircularCenter

# NEED TO GO THROUGH PRIVATE VARIABLES


def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular centre for the current data
    """
    if logger.check_if_all_needed(Flags.files_loaded):
        widget = CustomInputFormCircularCenter()
        widget.exec()
        sigma = widget._ui.sigma_value.value()
        rmms_1 = widget._ui.rmms1st.value()
        rmms_2 = widget._ui.rmms2nd.value()
        rmms_3 = widget._ui.rmms3rd.value()
        ApplicationWindow._cyx, ApplicationWindow.radius = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
                                                                                 sigma, rmms=(rmms_1, rmms_2, rmms_3))
        logger.log("Circular center has now been initialized", Flags.circular_center)


def remove_aperture(ApplicationWindow):
    """
    Generate aperture to limit region to BF disc. This will also allow the algorithm to go faster
    """
    if logger.check_if_all_needed(Flags.circular_center):
        widget = CustomInputRemoveAperture()
        widget.exec()
        sigma = widget._ui.sigma_val.value()
        add_radius = widget._ui.add_radius.value()
        aaf = widget._ui.aaf.value()

        ApplicationWindow.mm_sel = ApplicationWindow.ds_sel

        ApplicationWindow._ap = fpdp.synthetic_aperture(ApplicationWindow.mm_sel.shape[-2:],
                                                        ApplicationWindow._cyx,
                                                        rio=(0, ApplicationWindow.radius + add_radius),
                                                        sigma=sigma, aaf=aaf)[0]
        plot.matshow(ApplicationWindow._ap)
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
        com_yx = fpdp.center_of_mass(ApplicationWindow.mm_sel, nr, nc, thr='otsu',
                                     aperture=ApplicationWindow._ap, parallel=False)

        fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
        com_yx_cor = com_yx - fit
        # Convert to beta using the BF disc and calibration.
        # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
        # You may see that the aperture is not a perfect circle - error bars
        cyx_sp, r_sp = fpdp.find_circ_centre(ApplicationWindow._sum_dif,
                                             sigma=2,
                                             rmms=(ApplicationWindow.radius - 8,
                                                   ApplicationWindow.radius + 8, 1),
                                             spf=4)
        logger.log("Center of mass has now been found", Flags.center_mass)
        ApplicationWindow.com_yx_beta = com_yx_cor
