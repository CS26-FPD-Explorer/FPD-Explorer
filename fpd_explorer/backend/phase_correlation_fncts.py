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
from .. import logger
from ..logger import Flags
from .custom_fpd_lib import phase_correlation as pc
from ..frontend.gui_generator import UI_Generator
from ..frontend.custom_widgets import LoadingForm, Pop_Up_Widget


def find_matching_images(ApplicationWindow):
    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow, "Find Matching Images")
        avail_input = [("None", None)]
        ApplicationWindow.matching_input.update({"ds_sel[:10,:10]": ApplicationWindow.ds_sel[:10, :10]})
        try:
            assert ApplicationWindow.ap is not None
            avail_input.append(("aperture", ApplicationWindow.ap))
        except (AttributeError, AssertionError):
            pass

        key_add = {
            "aperture": ["multipleinput", avail_input, "An aperture to apply to the images."],
            "images": ["multipleinput", list(ApplicationWindow.matching_input.items()),
                       "Array of images with image axes in last 2 dimensions."]}

        params = UI_Generator(ApplicationWindow, pc.find_matching_images, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        results = params.get_result()
        results["widget"] = canvas
        if not results["plot"]:
            loading_widget = LoadingForm(2, ["NRSME", "NRSME-all"])
            loading_widget.setup_multi_loading(["NRSME", "NRSME-all"], pc.find_matching_images, **results)
            loading_widget.exec()
            ApplicationWindow.matching = loading_widget.get_result("matching")
        else:
            ApplicationWindow.matching = pc.find_matching_images(**results)
        logger.log("Found Matching images", Flags.phase_matching)


def disc_edge_sigma(ApplicationWindow):
    if logger.check_if_all_needed(Flags.phase_matching):
        canvas = Pop_Up_Widget(ApplicationWindow, "Disc Edge Sigma")
        ApplicationWindow.edge_input.update({"meaned_image": ApplicationWindow.matching.ims_common.mean(0)})
        try:
            assert ApplicationWindow.ap is not None
            ApplicationWindow.edge_input.update(
                {"mean with aperture": ApplicationWindow.ap * ApplicationWindow.matching.ims_common.mean(0)})
        except (AttributeError, AssertionError):
            pass
        key_add = {
            "im": ["multipleinput", list(ApplicationWindow.edge_input.items()), "Image of disc"]}

        params = UI_Generator(ApplicationWindow, pc.disc_edge_sigma, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return

        ApplicationWindow.edge_sigma = pc.disc_edge_sigma(**params.get_result(), widget=canvas, logger=logger)[0]
        logger.log("Found disk edge sigma")


def make_ref_im(ApplicationWindow):
    if logger.check_if_all_needed(Flags.phase_matching):
        canvas = Pop_Up_Widget(ApplicationWindow, "Make Reference Image")
        ApplicationWindow.ref_input.update({"meaned_image": ApplicationWindow.matching.ims_common.mean(0)})
        try:
            assert ApplicationWindow.ap is not None
            ApplicationWindow.ref_input.update(
                {"mean with aperture": ApplicationWindow.ap * ApplicationWindow.matching.ims_common.mean(0)})
        except (AttributeError, AssertionError):
            pass
        key_add = {
            "image": ["multipleinput", list(ApplicationWindow.ref_input.items()), " Image to process"]}

        params = UI_Generator(ApplicationWindow, pc.make_ref_im, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        ApplicationWindow.ref_im = pc.make_ref_im(**params.get_result(), widget=canvas)
        logger.log("Reference image created successfully")


def phase_correlation(ApplicationWindow):
    if logger.check_if_all_needed(Flags.files_loaded):
        canvas = Pop_Up_Widget(ApplicationWindow, "Phase Corelation")
        ApplicationWindow.phase_input.update({"ds_sel": ApplicationWindow.ds_sel})
        ref_image = {"None": None}
        try:
            ref_image.update({"Ref_im": ApplicationWindow.ref_im})
        except (AttributeError):
            pass

        key_add = {
            "ref_im": ["multipleinput", list(ref_image.items()), """2-D image used as reference.\n
                If None, the first probe position is used."""],
            "data": ["multipleinput", list(ApplicationWindow.phase_input.items()),
                     "Mutidimensional data of shape (scanY, scanX, ..., detY, detX)"]}

        params = UI_Generator(ApplicationWindow, pc.phase_correlation, key_add=key_add)

        if not params.exec():
            # Procedure was cancelled so just give up
            return
        print(params.get_result())
        out = pc.phase_correlation(**params.get_result(), logger=logger)
        ApplicationWindow.shift_yx, ApplicationWindow.shift_err = out[:2]
        ApplicationWindow.shift_difp, ApplicationWindow.ref = out[2:]
        logger.log("Phase Correlation finished sucessfully")
