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

# FPD Explorer
from ..backend import virtual_adf, dpc_explorer, fpd_functions, data_browser_explorer, phase_correlation_fncts
from .custom_widgets import Pop_Up_Widget, QIPythonWidget


def start_dbrowser(self):
    data_browser_explorer.start_dbrowser(self)


def start_dpc_explorer(self):
    dpc_explorer.start_dpc(self)


def start_vadf(self):
    virtual_adf.start_vadf(self)


def plot_vadf(self):
    virtual_adf.plot_vadf(self)


def annular_slice_vadf(self):
    virtual_adf.annular_slice(self)


def find_circular_centre(self):
    fpd_functions.find_circular_centre(self)


def remove_aperture(self):
    fpd_functions.remove_aperture(self)


def centre_of_mass(self):
    fpd_functions.centre_of_mass(self)


def ransac_im_fit(self):
    fpd_functions.ransac_im_fit(self)


def find_matching_images(self):
    phase_correlation_fncts.find_matching_images(self)


def disc_edge_sigma(self):
    phase_correlation_fncts.disc_edge_sigma(self)


def make_ref_im(self):
    phase_correlation_fncts.make_ref_im(self)


def phase_correlation(self):
    phase_correlation_fncts.phase_correlation(self)


def start_live_coding(self):
    if self.dark_mode_config:
        theme = "linux"
    else:
        theme = "LightBG"
    ipy_console = QIPythonWidget(self, colors=theme, font_size=11, kind='rich', syntax_styl='monokai')
    console_tab = Pop_Up_Widget(self, "Live Coding")
    console_tab.setup_docking_default(ipy_console)


def add_data(self, location, name, data):
    location = location.lower()
    if "dpc" in location:
        self.dpc_input.update({name: data})
    elif "circular" in location:
        self.circular_input.update({name: data})
    elif "data" in location:
        self.data_input.update({name: data})
    elif "nav" in location:
        self.nav_data_input.update({name: data})
    elif "mass" in location:
        self.mass_input.update({name: data})
    elif "ransac" in location:
        self.ransac_input.update({name: data})
    elif "matching" in location:
        self.matching_input.update({name: data})
    elif "edge" in location:
        self.edge_input.update({name: data})
    elif "ref" in location:
        self.ref_input.update({name: data})
    elif "phase" in location:
        self.phase_input.update({name: data})
    elif "vadf" in location:
        self.vadf_input.update({name: data})
