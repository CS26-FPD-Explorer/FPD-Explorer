# FPD_EXPLORER

from . import logger
from .logger import Flags
from .gui_generator import UI_Generator
from .custom_fpd_lib import fpd_processing as fpdp
from .custom_widgets import Pop_Up_Widget


def ransac_tools(ApplicationWindow):
    """Calculate **add here when you know**
    for the users input, and brings up two
    figures based on that input on the UI
    """

    # fit, inliers, _ = fpd.ransac_tools.ransac_im_fit(com_yx, residual_threshold=0.01, plot=True)
    if logger.check_if_all_needed(Flags.center_mass):
        return
