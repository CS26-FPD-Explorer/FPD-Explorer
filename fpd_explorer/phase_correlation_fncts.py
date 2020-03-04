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
        try:
            avail_input.append(("aperture", ApplicationWindow.ap))
        except AttributeError:
            pass

        key_add = {
            "aperture": ["multipleinput", avail_input, "An aperture to apply to the images."],
            "images": ["multipleinput", [
                ("ds_sel", ApplicationWindow.ds_sel[:10, 50:55])], "An aperture to apply to the images."]}

        params = UI_Generator(ApplicationWindow, fpdp.find_circ_centre, key_ignore=[], key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.matching = fpdp.find_matching_images(**params.get_result(),widget=canvas)


def disc_edge_sigma(ApplicationWindow):

    ApplicationWindow.edge_sigma = fpdp.disc_edge_sigma(image, sigma=2, cyx=cyx, r=cr, plot=True)[0]


def make_ref_im(ApplicationWindow):
    ApplicationWindow.ref_im = fpdp.make_ref_im(
        ApplicationWindow.image, edge_sigma=1.0, aperture=None, bin_opening=0, bin_closing=4, plot=True)


def phase_correlation(ApplicationWindow):
    ApplicationWindow.shift_yx, ApplicationWindow.shift_err, ApplicationWindow.shift_difp, ApplicationWindow.ref = pc.phase_correlation(
        ds_sel, nc=None, nr=None, spf=100, ref_im=ref_im, cyx=cyx, crop_r=cr + 3, sigma=si)
