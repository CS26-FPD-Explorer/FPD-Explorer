# FPD Explorer
from . import logger
from .logger import Flags
from .gui_generator import UI_Generator
from .custom_fpd_lib import ransac_tools as rt
from .custom_fpd_lib import fpd_processing as fpdp
from .custom_widgets import Pop_Up_Widget, SingleLoadingForm

# NEED TO GO THROUGH PRIVATE VARIABLES


def find_circular_centre(ApplicationWindow):
    """ Calculate the circular centre for the users input
    parameters, when function is used it will
    bring up a figure on a new tab, and switch to this
    tab.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """

    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow, "Circular Center")
        key_add = {
            "im": [
                "multipleinput", [
                    ("Image", ApplicationWindow._sum_im), ("Diffraction", ApplicationWindow._sum_dif)], "Test"]}

        params = UI_Generator(ApplicationWindow, fpdp.find_circ_centre, key_ignore=["im"], key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.cyx, ApplicationWindow.radius = fpdp.find_circ_centre(**params.get_result(), widget=canvas)
        logger.log("Circular center has now been initialized", Flags.circular_center)
        logger.log("Radius is : " + str(ApplicationWindow.radius))
        logger.log("Center (y, x) is : " + str(ApplicationWindow.cyx))


def remove_aperture(ApplicationWindow):
    """
    Generates a synthetic aperture for the users input
    parameters, when function is used it will
    bring up a figure on the UI in a new tab, and switch
    to this tab.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """

    if logger.check_if_all_needed(Flags.circular_center):
        key_add = {
            "rio": ["length2iterable", None, "Inner and outer radii [ri,ro) in a number of forms"]
        }
        params = UI_Generator(ApplicationWindow, fpdp.synthetic_aperture, key_ignore=["shape"], key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return

        ApplicationWindow.mm_sel = ApplicationWindow.ds_sel
        ApplicationWindow._ap = fpdp.synthetic_aperture(
            ApplicationWindow.mm_sel.shape[-2:], **params.get_result())[0]
        print(ApplicationWindow._ap)
        canvas = Pop_Up_Widget(ApplicationWindow, "Aperture")
        fig = canvas.setup_docking("Aperture")
        ax = fig.get_fig().subplots()
        ax.matshow(ApplicationWindow._ap)
        logger.log("Aperture has now been correctly initialized", Flags.aperture)


def centre_of_mass(ApplicationWindow):
    """
    calculates center of mass statistics based on the
    data set provided and the previous functions run.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """
    if logger.check_if_all_needed(Flags.aperture):
        key_add = {
            "aperture": ["bool", True, """Should an aperture be provided \n
            If yes then the output of remove aperture shall be used"""]
        }
        params = UI_Generator(ApplicationWindow, fpdp.center_of_mass, key_ignore=["data", "aperture"], key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()
        if results["aperture"] == True:
            # Replace the bool with the variable
            results["aperture"] = ApplicationWindow._ap
        else:
            # Remove aperture in this case since its a bool and they expect an array
            results.pop("aperture")
        loading_widget = SingleLoadingForm(fpdp.center_of_mass, ApplicationWindow.mm_sel, **results, thr='otsu')
        loading_widget.exec()
        ApplicationWindow.com_yx = loading_widget.com_yx

        # TODO: Fix the mess in another feature
        # fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
        # com_yx_cor = com_yx - fit
        # Convert to beta using the BF disc and calibration.
        # The pixel value radius from before could be used for the calibration, or we can do a subpixel equivalent.
        # You may see that the aperture is not a perfect circle - error bars
        # cyx_sp, r_sp = fpdp.find_circ_centre(ApplicationWindow._sum_dif, sigma=2,
        #                                     rmms=(ApplicationWindow.radius-8, ApplicationWindow.radius+8, 1), spf=4)
        logger.log("Center of mass has now been found", Flags.center_mass)
        ApplicationWindow.com_yx_beta = ApplicationWindow.com_yx


def ransac_im_fit(ApplicationWindow):
    """
    once center of mass has been run, function runs
    with the users input, and brings up a figure on
    based on that input on the UI, switches to tab
    showing the data.


    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """

    # fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
    if logger.check_if_all_needed(Flags.center_mass):
        # FIXME: Dirty fix to prevent float overloading the int and messing it up
        # Will be fixed by next commit in another branch
        key_add = {
            "min_samples": ["int", 10, """
            The minimum number of data points to fit a model to.\n
            If an int, the value is the number of pixels.\n
            If a float, the value is a fraction (0.0, 1.0] of the total number of pixels."""]
        }
        canvas = Pop_Up_Widget(ApplicationWindow, "Aperture")
        params = UI_Generator(
            ApplicationWindow,
            rt.ransac_im_fit,
            key_ignore=["im", "plot", "min_samples", "p0"],
            key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()
        fit, inliers, _ = rt.ransac_im_fit(ApplicationWindow.com_yx, **results, plot=True, widget=canvas)
        ApplicationWindow.com_yx_cor = ApplicationWindow.com_yx - fit
        logger.log("Image has now been fitted using ransac")
