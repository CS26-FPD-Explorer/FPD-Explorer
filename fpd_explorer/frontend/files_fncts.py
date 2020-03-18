# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

import h5py
from PySide2.QtWidgets import QFileDialog

# FPD Explorer
from .. import logger
from ..logger import Flags


def open_mib(self):
    """
    Spawn a file dialog to open an mib file
    """
    fname, _ = QFileDialog.getOpenFileName(
        self, 'Open file', self._last_path,
        "Merlin Binary files (*.mib)")
    if fname:
        if fname[-3:] == "mib":  # empty string means user cancelled
            self._update_last_path(fname)
            self._mib_path = fname
            self._ui.mib_line.clear()
            self._ui.mib_line.insert(fname[fname.rfind('/') + 1:])
            logger.log("MIB file loaded correctly")
            return True
    return False


def open_npz(self):
    """
    Spawn a file dialog to open an npz file
    """
    try:
        fname = self.npz_path
    except AttributeError:
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path,
            "NPZ files (*.npz)")
    if fname:
        if fname[-3:] == "npz":  # empty string means user cancelled
            self._update_last_path(fname)
            self.npz_path = fname
            self._ui.npz_line.clear()
            self._ui.npz_line.insert(fname[fname.rfind('/') + 1:])
            logger.log("NPZ file loaded correctly", Flags.npz_loaded)
            return True
    return False


def open_hdf5(self):
    """
    Spawn a file dialog to open a hdf5 file
    """
    try:
        fname = self.hdf5_path
    except AttributeError:
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', self._last_path,
            "Hierarchical Data files (*.hdf5)")
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
            logger.log("HDF5 file loaded correctly", Flags.hdf5_usage)
            logger.add_flag(Flags.files_loaded)
            return True
    return False


def open_dm3(self):
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
            logger.log("DM3 file loaded correctly")
            return True
    return False
