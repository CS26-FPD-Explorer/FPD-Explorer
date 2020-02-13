import fpd
import scipy as sp

from .custom_fpd_lib import dpc_explorer_class as dpc
from .custom_widgets import Pop_Up_Widget


def start_dpc(ApplicationWindow):
    """
    Start the DPC Explorer and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QtWidgets.QApplication() the parent in which the tab should be rendered

    """
    dpc_explorer = Pop_Up_Widget(ApplicationWindow, "DPC Explorer")
    bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    bt = sp.ndimage.rotate(bt, angle=0.0, axes=(-2, -1),
                           reshape=False, order=3, mode='constant', cval=0.0, prefilter=True)

    DE = dpc.DPC_Explorer(bt, cyx=(0, 0), vectrot=125, gaus=0.0, pct=0.5, widget=dpc_explorer)

    # TODO implement error message
