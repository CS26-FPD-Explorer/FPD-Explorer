# FPD Explorer

from .. import logger
from ..logger import Flags
from .custom_fpd_lib import virtual_annular as va
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import Pop_Up_Widget

VADF = None


def start_vadf(ApplicationWindow):
    global VADF
    params = UI_Generator(ApplicationWindow, va.VirtualAnnularImages, key_ignore=["data"])
    if not params.exec():
        # Procedure was cancelled so just give up
        return
    results = params.get_result()

    if logger.check_if_all_needed(Flags.npz_loaded, display=False):
        VADF = va.VirtualAnnularImages(ApplicationWindow.npz_path, **results)
    else:  # No need for an elif because we want to handle all the case if the next if is false
        if logger.check_if_all_needed(Flags.circular_center):
            if logger.check_if_all_needed(Flags.files_loaded):
                if logger.check_if_all_needed(Flags.hdf5_usage, display=False):
                    ds = ApplicationWindow._ds
                else:
                    ds = ApplicationWindow.ds_sel
                VADF = va.VirtualAnnularImages(ds, **results)
        else:
            return
    logger.log("VADF initialized correctly", Flags.vadf_init)


def plot_vadf(ApplicationWindow):
    if logger.check_if_all_needed(Flags.vadf_init):
        hdf5_usage = logger.check_if_all_needed(Flags.hdf5_usage, display=False)
        if hdf5_usage or logger.check_if_all_needed(Flags.files_loaded):
            vadf_explorer = Pop_Up_Widget(ApplicationWindow, "VADF_Explorer")
            VADF.plot(nav_im=ApplicationWindow.sum_dif, widget=vadf_explorer)


def annular_slice(ApplicationWindow):
    if logger.check_if_all_needed(Flags.vadf_init):
        params = UI_Generator(ApplicationWindow, VADF.annular_slice)
        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()

        vadf = VADF.annular_slice(**results)
        canvas = Pop_Up_Widget(ApplicationWindow, "Annular Slice")
        fig = canvas.setup_docking("Annular Slice")
        ax = fig.get_fig().subplots()
        ax.matshow(vadf)
