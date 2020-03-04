import fpd.fpd_processing as fpdp

# FPD Explorer
from . import logger
from .logger import Flags
from .gui_generator import UI_Generator
from .custom_fpd_lib import phase_correlation as pc
from .custom_widgets import Pop_Up_Widget


def find_matching_images(ApplicationWindow):
    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow, "Find Matching Images")
        avail_input = [("None", None)]
        ApplicationWindow.matching_input.update({"ds_sel[:10,:10]": ApplicationWindow.ds_sel[:10, :10]})
        try:
            assert ApplicationWindow.ap is not None
            avail_input.append(("aperture", ApplicationWindow.ap))
        except (AttributeError, AssertionError):
            pass
        
        key_add = {
            "aperture": ["multipleinput", avail_input, "An aperture to apply to the images."],
            "images": ["multipleinput", list(ApplicationWindow.matching_input.items()), 
                       "Array of images with image axes in last 2 dimensions."]}

        params = UI_Generator(ApplicationWindow, pc.find_matching_images, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.matching = pc.find_matching_images(**params.get_result(), widget=canvas)
        logger.log("Found Matching images", Flags.phase_matching)


def disc_edge_sigma(ApplicationWindow):
    if logger.check_if_all_needed(Flags.phase_matching):
        canvas = Pop_Up_Widget(ApplicationWindow, "Disc Edge Sigma")
        ApplicationWindow.edge_input.update({"meaned_image": ApplicationWindow.matching.ims_common.mean(0)})
        try:
            assert ApplicationWindow.ap is not None
            ApplicationWindow.edge_input.update(
                {"mean with aperture", ApplicationWindow.ap * ApplicationWindow.matching.ims_common.mean(0)})
        except (AttributeError, AssertionError):
            pass
        key_add = {
            "im": ["multipleinput", list(ApplicationWindow.edge_input.items()), "Image of disc"]}

        params = UI_Generator(ApplicationWindow, pc.disc_edge_sigma, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return

        ApplicationWindow.edge_sigma = pc.disc_edge_sigma(**params.get_result(), widget=canvas)[0]


def make_ref_im(ApplicationWindow):
    if logger.check_if_all_needed(Flags.phase_matching):
        canvas = Pop_Up_Widget(ApplicationWindow, "Make Reference Image")
        ApplicationWindow.ref_input.update({"meaned_image": ApplicationWindow.matching.ims_common.mean(0)})
        try:
            assert ApplicationWindow.ap is not None
            ApplicationWindow.ref_input.update(
                {"mean with aperture", ApplicationWindow.ap * ApplicationWindow.matching.ims_common.mean(0)})
        except (AttributeError, AssertionError):
            pass
        key_add = {
            "image": ["multipleinput", list(ApplicationWindow.ref_input.items()), " Image to process"]}

        params = UI_Generator(ApplicationWindow, pc.make_ref_im, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.ref_im = pc.make_ref_im(**params.get_result(), widget=canvas)


def phase_correlation(ApplicationWindow):
    ApplicationWindow.shift_yx, ApplicationWindow.shift_err, ApplicationWindow.shift_difp, ApplicationWindow.ref = pc.phase_correlation(
        ds_sel, nc=None, nr=None, spf=100, ref_im=ref_im, cyx=cyx, crop_r=cr + 3, sigma=si)
