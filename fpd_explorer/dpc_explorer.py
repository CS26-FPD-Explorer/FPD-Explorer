from .custom_fpd_lib import dpc_explorer_class as dpc
import scipy as sp

import fpd

def start_dpc(ApplicationWindow):

    bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    bt = sp.ndimage.rotate(bt, angle=0.0, axes=(-2, -1), reshape=False, order=3, mode='constant', cval=0.0, prefilter=True)
    DE = dpc.DPC_Explorer(bt, cyx=(0, 0), vectrot=125, gaus=0.0, pct=0.5)
