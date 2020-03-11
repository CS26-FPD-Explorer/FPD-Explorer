from fpd_explorer.frontend.custom_widgets import CustomInputForm
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


def init_inputbox():
    """
    Creating an inputbox.ui similar to those one that is used to scale the size
    of the input data.
    """
    return CustomInputForm(initial_x=2, initial_y=2, minimum=0, maximum=13, text_x='', text_y='')


def test_input_form_size_maximum(qtbot):
    """
    Testing Xsize and Ysize has a maximum value set. This means that we can't reduce the size
    of the data by large amounts affecting the quality of the visualisation produced.
    """
    widget = init_inputbox()
    widget._ui.Xsize.setValue(14)
    widget._ui.Ysize.setValue(14)
    assert (widget._ui.Xsize.value() > widget._ui.Xsize.maximum()) == False
    assert (widget._ui.Ysize.value() > widget._ui.Ysize.maximum()) == False


def test_input_form_restore_to_default(qtbot):
    """
    Testing that the restore to default function that is binded to the Restore Default
    button resets the values correctly.
    """
    widget = init_inputbox()
    widget._ui.Xsize.setValue(10)
    widget._ui.Ysize.setValue(10)
    widget.restore_default()
    assert widget._ui.Xsize.value() == 2
    assert widget._ui.Ysize.value() == 2
