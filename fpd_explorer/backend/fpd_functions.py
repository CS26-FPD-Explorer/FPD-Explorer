# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

# FPD Explorer
from .. import logger
from ..logger import Flags
from .custom_fpd_lib import ransac_tools as rt
from .custom_fpd_lib import fpd_processing as fpdp
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import LoadingForm, Pop_Up_Widget


def find_circular_centre(ApplicationWindow):
    """
    Calculate the circular centre from the user input parameters,
    create a figure in a new tab and switch to the tab.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """

    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow, "Circular Center")
        ApplicationWindow.circular_input.update({"Image": ApplicationWindow.sum_im,
                                                 "Diffraction": ApplicationWindow.sum_dif})
        key_add = {
            "im": [
                "multipleinput", list(ApplicationWindow.circular_input.items()), "Image data"]
        }

        params = UI_Generator(ApplicationWindow, fpdp.find_circ_centre, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.cyx, ApplicationWindow.radius = fpdp.find_circ_centre(**params.get_result(), widget=canvas)
        logger.log("Circular center has now been initialized", Flags.circular_center)
        logger.log("Radius is : " + str(ApplicationWindow.radius))
        logger.log("Center (y, x) is : " + str(ApplicationWindow.cyx))


def remove_aperture(ApplicationWindow):
    """
    Generate a synthetic aperture from the user input parameters,
    create a figure in a new tab and switch to the tab.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """

    if logger.check_if_all_needed(Flags.circular_center):
        key_add = {
            "rio": [
                "length2iterable",
                (0,
                 ApplicationWindow.radius + 8),
                "Inner and outer radii [ri,ro) in a number of forms"],
            "cyx": [
                "length 2 iterable",
                tuple(
                    ApplicationWindow.cyx),
                "Centre y, x pixel cooridinates"]}
        params = UI_Generator(ApplicationWindow, fpdp.synthetic_aperture, key_ignore=["shape"], key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return

        ApplicationWindow.mm_sel = ApplicationWindow.ds_sel
        ApplicationWindow.ap = fpdp.synthetic_aperture(
            ApplicationWindow.mm_sel.shape[-2:], **params.get_result())[0]
        canvas = Pop_Up_Widget(ApplicationWindow, "Aperture")
        fig = canvas.setup_docking("Aperture")
        ax = fig.get_fig().subplots()
        ax.matshow(ApplicationWindow.ap)
        logger.log("Aperture has now been correctly initialized", Flags.aperture)


def centre_of_mass(ApplicationWindow):
    """
    Calculate center of mass statistics based on the
    dataset provided and the previous functions run.

    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """
    if logger.check_if_all_needed(Flags.aperture):
        ApplicationWindow.mass_input.update({"mm_sel": ApplicationWindow.mm_sel})

        key_add = {
            "aperture": [
                "bool",
                True,
                """Should an aperture be provided \n
            If yes then the output of remove aperture shall be used"""],
            "data": [
                "multipleinput",
                list(
                    ApplicationWindow.mass_input.items()),
                "Mutidimensional data of shape (scanY, scanX, ..., detY, detX)"]}

        params = UI_Generator(ApplicationWindow, fpdp.center_of_mass, key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()
        if results["aperture"] == True:
            # Replace the bool with the variable
            results["aperture"] = ApplicationWindow.ap
        else:
            # Remove aperture in this case since its a bool and they expect an array
            results.pop("aperture")
        loading_widget = LoadingForm(1, ["com_yx"])
        loading_widget.setup_multi_loading("com_yx", fpdp.center_of_mass, **results)
        loading_widget.exec()
        ApplicationWindow.com_yx = loading_widget.get_result("com_yx")
        logger.log("Center of mass has now been found", Flags.center_mass)
        logger.log(fpdp.print_shift_stats(ApplicationWindow.com_yx, to_str=True))
        ApplicationWindow.com_yx_beta = ApplicationWindow.com_yx


def ransac_im_fit(ApplicationWindow):
    """
    Check if center of mass has been calculated. If True,
    fit an image using ransac from the user input parameters,
    create a figure in a new tab and switch to the tab.


    Parameters
    ----------
    ApplicationWindow : QApplication
        intialises the application with the user's desktop settings,
        performs event handling
    """
    if logger.check_if_all_needed(Flags.center_mass):

        ApplicationWindow.ransac_input.update({"com_yx": ApplicationWindow.com_yx})
        key_add = {
            "im": [
                "multipleinput", list(ApplicationWindow.ransac_input.items()), "ndarray with images to fit to."],
            "min_samples": ["int", 10, """
            The minimum number of data points to fit a model to.\n
            If an int, the value is the number of pixels.\n
            If a float, the value is a fraction (0.0, 1.0] of the total number of pixels."""]
        }
        canvas = Pop_Up_Widget(ApplicationWindow, "Aperture")
        params = UI_Generator(
            ApplicationWindow,
            rt.ransac_im_fit,
            key_ignore=["plot", "min_samples", "p0"],
            key_add=key_add)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()
        fit, inliers, _ = rt.ransac_im_fit(**results, plot=True, widget=canvas)
        ApplicationWindow.com_yx_cor = ApplicationWindow.com_yx - fit
        logger.log("Image has now been fitted using ransac")
