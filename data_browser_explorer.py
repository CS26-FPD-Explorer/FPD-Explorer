from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog

from fpd.fpd_file import MerlinBinary
from custom_widgets import CustomInputForm, CustomLoadingForm
from data_browser_new import DataBrowserNew


def load_files(ApplicationWindow):
    """
    setp up the databrowser and open the file if not present
    """
    x_value = None
    y_value = None
    # Cherk if Mib exist
    try:
        mib = ApplicationWindow._mib_path
    except AttributeError:
        response = QtWidgets.QMessageBox.warning(
            ApplicationWindow, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes)
        if response == QtWidgets.QMessageBox.Yes:
            valid = ApplicationWindow.function_mib()  # load a .mib file and use it
            if not valid:  # user canceled
                return
        else:
            return

    mib = ApplicationWindow._mib_path
    # Check if dm3 exist
    try:
        dm3 = ApplicationWindow._dm3_path
    except AttributeError:
        dm3 = []
        response = QtWidgets.QMessageBox.warning(
            ApplicationWindow, "Warning", "<strong>We noticed you don't have a Digital Micrograph files</strong> <br> Do you want to select one ?",
            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes)
        if response == QtWidgets.QMessageBox.Cancel:  # do nothing
            return
        elif response == QtWidgets.QMessageBox.Yes:
            valid = ApplicationWindow.function_dm3()  # load a .DM3 file and use it
            if not valid:  # user canceled
                return
            dm3 = ApplicationWindow._dm3_path
        else:  # load the data using custum parameter
            x, y = input_form(initial_x=8, initial_y=8, minimum=2)
            x_value = (x, 'x', 'na')
            y_value = (y, 'y', 'na')

    hdr = ApplicationWindow._mib_path[:-4]+".hdr"
    ApplicationWindow._mb = MerlinBinary(mib, hdr, dm3, scanYalu=y_value,
                            scanXalu=x_value, row_end_skip=1)

    ApplicationWindow._ds = ApplicationWindow._mb.get_memmap()

    x, y = input_form(initial_x=3, initial_y=3, text_x="Amount to skip for Navigation Image",
                            text_y="Amount to skip for Diffraction Image")  # Check what i sthe maximum value
    real_skip = x
    recip_skip = y
    print("skipping : " + str(x) + " " + str(y))
    # real_skip, an integer, real_skip=1 loads all pixels, real_skip=n an even integer downsamples
    # Obvious values are 1 (no down-sample), 2, 4

    # Assign the down-sampled dataset
    ApplicationWindow.ds_sel = ApplicationWindow._ds[::real_skip,
                            ::real_skip, ::recip_skip, ::recip_skip]
    # remove # above to reduce total file loading - last indice is amount to skip by.
    # Coordinate order is y,x,ky,kx
    # i.e. reduce real and recip space pixel count in memory

    widget = CustomLoadingForm(ApplicationWindow.ds_sel)
    widget.exec()

    # Set the value to default
    scanY, scanX = ApplicationWindow.ds_sel.shape[:2]
    ApplicationWindow._ui.navX.setValue(scanX//64 if scanX//64 != 0 else 1)
    ApplicationWindow._ui.navY.setValue(scanY//64 if scanY//64 != 0 else 1)
    ApplicationWindow._ui.navX.setMaximum(scanX)
    ApplicationWindow._ui.navY.setMaximum(scanY)

    ApplicationWindow._sum_dif = widget._sum_dif
    ApplicationWindow._sum_im = widget._sum_im

    ApplicationWindow._data_browser = DataBrowserNew(ApplicationWindow.ds_sel, nav_im=ApplicationWindow._sum_im,
                                        widget_1=ApplicationWindow._ui.navCanvas, widget_2=ApplicationWindow._ui.diffCanvas)

    ApplicationWindow._ui.colorMap.setCurrentIndex(0)

def input_form(initial_x=2, initial_y=2, minimum=0, maximum=13, text_x=None, text_y=None):
    """
    create an input form with the given value
    Parameters
    ----------
    initial_x int value the top value should start from
    initial_y int value the bottom value should start from
    minimum int minimum value the spin box should be allowed to go
    maximum int maximum value the spin box should be allowed to go
    text_x str Text to set in the top screen
    text_y str Text to set in the bottom screen

    """

    widget = CustomInputForm(initial_x, initial_y,
                                minimum, maximum, text_x, text_y)
    widget.exec()
    x = pow(2, widget._ui.Xsize.value())
    y = pow(2, widget._ui.Ysize.value())
    return x, y
