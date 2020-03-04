import h5py
from PySide2.QtWidgets import QFileDialog

# FPD Explorer
from . import logger
from .logger import Flags


def function_mib(self):
    """
    Spawn a file dialog to open an mib file
    """
    fname, _ = QFileDialog.getOpenFileName(
        self, 'Open file', self._last_path,
        "MERLIN binary files (*.mib)")
    if fname:
        if fname[-3:] == "mib":  # empty string means user cancelled
            self._update_last_path(fname)
            self._mib_path = fname
            self._ui.mib_line.clear()
            self._ui.mib_line.insert(fname[fname.rfind('/') + 1:])
            logger.log("MIB file correctly loaded")
            return True
    return False


def function_npz(self):
    """
    Spawn a file dialog to open an npz file
    """
    fname, _ = QFileDialog.getOpenFileName(
        self, 'Open file', self._last_path,
        "NPZ file (*.npz)")
    if fname:
        if fname[-3:] == "npz":  # empty string means user cancelled
            self._update_last_path(fname)
            self.npz_path = fname
            self._ui.npz_line.clear()
            self._ui.npz_line.insert(fname[fname.rfind('/') + 1:])
            logger.log("NPZ file correctly loaded", Flags.npz_loaded)
            return True
    return False


def function_hdf5(self):
    """
    Spawn a file dialog to open an hdf5 file
    """
    fname, _ = QFileDialog.getOpenFileName(
        self, 'Open file', self._last_path,
        "MERLIN binary files (*.hdf5)")
    if fname:
        if fname[-4:] == "hdf5":  # empty string means user cancelled
            self._update_last_path(fname)
            self.hdf5_path = fname
            self._ui.hdf5_line.clear()
            self._ui.hdf5_line.insert(fname[fname.rfind('/') + 1:])
            f = h5py.File(fname, 'r')
            self.ds = f['fpd_expt/fpd_data/data']
            self.ds_sel = self.ds
            self.sum_im = f['fpd_expt/fpd_sum_im/data'].value
            self.sum_dif = f['fpd_expt/fpd_sum_dif/data'].value
            logger.log("HDF5 file correctly loaded", Flags.hdf5_usage)
            logger.add_flag(Flags.files_loaded)
            return True
    return False


def function_dm3(self):
    """
    Spawn a file dialog to open a dm3 file
    """
    fname, _ = QFileDialog.getOpenFileName(
        self, 'Open file', self._last_path,
        "Digital Micrograph files (*.dm3)")
    if fname:
        if fname[-3:] == "dm3":
            self._update_last_path(fname)
            self._dm3_path = fname
            self._ui.dm3_line.clear()
            self._ui.dm3_line.insert(fname[fname.rfind('/') + 1:])
            logger.log("DM3 file correctly loaded")
            return True
    return False
