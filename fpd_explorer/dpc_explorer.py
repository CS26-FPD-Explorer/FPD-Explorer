import fpd
import scipy as sp

# FPD Explorer
from .gui_generator import UI_Generator
from .custom_fpd_lib import dpc_explorer_class as dpc
from .custom_widgets import Pop_Up_Widget


def start_dpc(ApplicationWindow):
    """
    Start the DPC Explorer and switch to that tab if the files are loaded.
    Otherwise display an error

    Parameters
    ----------
    ApplicationWindow : QApplication
        Parent in which the tab should be rendered

    """
    dpc_explorer = Pop_Up_Widget(ApplicationWindow, "DPC Explorer")
    avail_input = []
    try:
        avail_input.append(("cyx", ApplicationWindow.cyx))
    except AttributeError:
        pass
    try:
        avail_input.append(("com_yx_beta", ApplicationWindow.com_yx_beta))
        avail_input.append(("beta2bt", fpd.mag_tools.beta2bt(
            ApplicationWindow.com_yx_beta) * 1e9))
    except AttributeError:
        pass
    try:
        avail_input.append(("ransac", ApplicationWindow.com_yx_cor))
    except AttributeError:
        pass

    if len(avail_input) == 0:
        raise Exception("""No data found that could be used with DPC Explorer.\n
        Please run some function before trying again""")
    key_add = {
        "d": [
            "multipleinput", avail_input, """If array-like, yx data. If length 2 iterable or ndarray of \n
                    shape (2, M, N), data is single yx dataset. If shape is \n
                    (S, 2, M, N), a sequence yx data of length S can be plotted."""],
        "rotate": [
            "bool", False, "rotate image if needed. This can make data interpretation easier"],
        "hist_lims": [
            "togglevalue", ["length4tupleofscalars,orNone", None,
                            """Histogram limits in order of xmin, xmax, ymin, ymax.\n
                                If None, limits are taken from data."""],
            """Check if you want to manually set the hist lim"""],
        "descan": [
            "togglevalue", ["length 4 iterable", [0, 0, 0, 0], """Plane descan correction.\n
                            [Yy, Yx, Xy, Xx] entered in 1/1000 for for convenience."""],
            """Check if you want to manually set the descan"""
        ]}

    params = UI_Generator(ApplicationWindow, dpc.DPC_Explorer, key_ignore=[
                          "r_min", "r_max", "median", "flip_y", "flip_x", "ransac"], key_add=key_add)
    if not params.exec():
        # Procedure was cancelled so just give up
        return
    results = params.get_result()
    print(results)
    # bt = fpd.mag_tools.beta2bt(ApplicationWindow.com_yx_beta) * 1e9  # T*nm

    # rotate image if needed. This can make data interpretation easier.
    if results.pop("rotate"):
        rot_params = UI_Generator(ApplicationWindow, sp.ndimage.rotate, key_ignore=["input"])
        if not rot_params.exec():
            # Procedure was cancelled so just give up
            return
        rot_results = rot_params.get_result()
        results["d"] = sp.ndimage.rotate(results["d"], **rot_results)
    DE = dpc.DPC_Explorer(**results, widget=dpc_explorer)
