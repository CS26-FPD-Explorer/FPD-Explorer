from __future__ import print_function

import collections
import datetime
import itertools
import multiprocessing as mp
import os
import sys
import time
import warnings
from collections import namedtuple
from functools import partial
from itertools import combinations
from numbers import Number

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.ndimage.filters import gaussian_filter, gaussian_filter1d
#from scipy.ndimage.measurements import center_of_mass
from scipy.signal import fftconvolve
from skimage import color
from skimage.draw import circle_perimeter
from skimage.feature import canny, peak_local_max, register_translation
#from skimage.transform import pyramid_expand
from skimage.filters import threshold_otsu
from skimage.morphology import binary_closing, binary_opening, disk
from skimage.transform import hough_circle
from tqdm import tqdm
import fpd
from fpd import fpd_processing as fpdp
from fpd import _p3


class VirtualAnnularImages(object):
    '''
    Fast virtual annular aperture image class using cumulative sums to
    calculate all data only once, and also provides interactive plotting.

    To do this, it uses: `fpd.fpd_processing.radial_average` and
    `fpd.fpd_processing.map_image_function`. See those functions for details
    not documented below.

    This method is very fast and so useful for exploring, but is not as
    flexible or accurate as `fpd.fpd_processing.synthetic_images`.

    The accuracy is typically a few percent with 'spf=1'. It can be made
    to be more accurate at the expense of computation time by increasing the 
    subpixel evaluation of the radial distribution through the `spf` parameter.

    Parameters
    ----------
    data : ndarray or string or dict
        If ndarray, `data` is the data to be processed, as defined in the
        fpd.fpd_processing.map_image_function. If a string, it should be the
        filename of a npz file with the parameters saved from the `save_data`
        method. If a dictionary, it must contain the same parameters.
    nr : integer or None
        Number of rows to process at once (see Notes).
    nc : integer or None
        Number of columns to process at once (see Notes).
    cyx : length 2 iterable or None
        The centre y and x coordinates of the direct beam in pixels.
        This value must be specified unless `data` is an object to be loaded. 
    parallel : bool
        If True, the calculations are multiprocessed.
    ncores : None or int
        Number of cores to use for mutliprocessing. If None, all cores
        are used.
    print_stats : bool
        If True, calculation progress is printed to stdout.
    nrnc_are_chunks : bool
        If True, `nr` and `nc` are interpreted as the number of chunks to
        process at once. If `data` is not chunked, `nr` and `nc` are used
        directly.
    spf : float
        The accuracy is typically a few percent with 'spf=1'. It can be made
        to be more accurate at the expense of computation time by increasing the 
        subpixel evaluation of the radial distribution
    '''
    def __init__(self, data, nr=16, nc=16, cyx=None, parallel=True, ncores=None,
                 nrnc_are_chunks=False, print_stats=True, mask=None, spf=1):
        

        self.r1 = None
        self.r2 = None
        self.virtual_image = None

        if _p3:
            s_obj = str
        else:
            s_obj = basestring

        if isinstance(data, s_obj):
            # add data filename attribute and load data as dict
            self._source_filename = data
            data = dict(np.load(data))
        if isinstance(data, dict):
            # add attributes
            for k, v in data.items():
                setattr(self, k, v)
        else:
            # process data to generate attributes
            if cyx is None:
                raise TypeError('cyx must be specified')
            self.data_shape = np.array(data.shape)
            self.cyx = np.array(cyx)
            self._calc_rdf(data, nr, nc, cyx, mask, spf, parallel, ncores,
                           nrnc_are_chunks, print_stats)

        # cummulative sums
        self.rms_cs = np.cumsum(self.rms * 2 * np.pi * self.r_pix[:, None, None], axis=0)
        self.a_cs = np.cumsum(2 * np.pi * (self.r_pix), axis=0)

    def save_data(self, filename=None):
        '''
        Save the calculated parameters to file for later reloading through the `data`
        initialisation parameter.

        Parameters
        ----------
        filename : None or string
            File name to save data under. If None a date stamped filename is generated.
            If the file name does not end in '.npz', it is automatically added.
        '''

        version = 1

        if filename is None:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = 'VirtualAnnularImages_' + now
        if filename.endswith('.npz') is False:
            filename = filename + '.npz'

        np.savez(filename,
                 data_shape=self.data_shape,
                 cyx=self.cyx,
                 r_pix=self.r_pix,
                 rms=self.rms,
                 version=version)
        print('Data saved to: %s' % (filename))

    def _calc_rdf(self, data, nr, nc, cyx, mask, spf, parallel, ncores,
                  nrnc_are_chunks, print_stats):
        rtn = fpdp.map_image_function(data, nr, nc,
                                 cyx=cyx,
                                 crop_r=None,
                                 func=fpdp.radial_average,
                                 params={'cyx': cyx, 'mask': mask, 'spf': spf},
                                 rebin=None,
                                 parallel=parallel,
                                 ncores=ncores,
                                 nrnc_are_chunks=nrnc_are_chunks,
                                 print_stats=print_stats)

        r_pix, rms = rtn.reshape((2, -1) + rtn.shape[1:])

        # 1-D
        self.r_pix = np.squeeze(r_pix[:, 0, 0])
        # rdf, scanY, scanX
        if rms.ndim == 4:
            # colour
            rms = rms[..., 0]

        self.rms = rms
        del rtn

    def annular_slice(self, r1, r2):
        '''
        Calculate an annular virtual image.

        Parameters
        ----------
        r1 : scalar
            Inner radius of aperture in pixels.
        r2 : scalar
            Inner radius of aperture in pixels.

        Returns
        -------
        virtual_image : ndarray
            The virtual image.

        '''
        self.r1 = r1
        self.r2 = r2

        r1i = np.argmax(self.r_pix >= r1)
        r2i = np.argmin(self.r_pix <= r2) - 1
        v = self.rms_cs[r2i] - self.rms_cs[r1i]
        va = self.a_cs[r2i] - self.a_cs[r1i]
        n = np.pi * (r2**2 - r1**2) / va
        self.virtual_image = v * n

        return self.virtual_image

    def plot(self, r1=None, r2=None, nav_im=None, norm='log', scroll_step=1, alpha=0.3, cmap=None, pct=0.1,
             mradpp=None, widget=None):
        '''
        Interactive plotting of the virtual aperture images.

        The sliders control the parameters and may be clicked, dragged or scrolled.
        Clicking on inner (r1) and outer (r2) slider labels sets the radii values
        to the minimum and maximum, respectively.

        Parameters
        ----------
        r1 : scalar
            Inner radius of aperture in pixels.
        r2 : scalar
            Inner radius of aperture in pixels.
        nav_im : None or ndarray
            Image used for the navigation plot. If None, a blank image is used.
        norm : None or string:
            If not None and norm='log', a logarithmic cmap normalisation is used.
        scroll_step : int
            Step in pixels used for each scroll event.
        alpha : float
            Alpha for aperture plot in [0, 1].
        cmap : None or a matplotlib colormap
            If not None, the colormap used for both plots.
        pct : scalar
            Slice image percentile in [0, 50).
        mradpp : None or scalar
            mrad per pixel.
        widget : Pop_Up_Widget
            A custom class consisting of mutliple widgets

        '''

        from matplotlib.widgets import Slider

        self._scroll_step = max([1, int(scroll_step)])
        self._pct = pct

        if norm is not None:
            if norm.lower() == 'log':
                from matplotlib.colors import LogNorm
                norm = LogNorm()

        # condition rs
        if r1 is not None:
            self.r1 = r1
        else:
            if self.r1 is None:
                self.r1 = 0
        if r2 is not None:
            self.r2 = r2
        else:
            if self.r2 is None:
                self.r2 = int((self.data_shape[-2:] / 4).mean())
        self.rc = (self.r2 + self.r1) / 2.0

        if nav_im is None:
            nav_im = np.zeros(self.data_shape[-2:])

        # calculate data
        virtual_image = self.annular_slice(self.r1, self.r2)
        print("MRADPP",mradpp)
        # prepare plots
        if mradpp is None:
            if widget is not None:
                print("True")
                docked = widget.setup_docking("Virtual Annular", "Bottom", figsize=(8.4, 4.8))
                fig = docked.get_fig()
                fig.clf()
                (ax_nav, ax_cntrst) = fig.subplots(1, 2)
                self._f_nav = fig
            else:
                self._f_nav, (ax_nav, ax_cntrst) = plt.subplots(1, 2, figsize=(8.4, 4.8))

        else:
            # add 2nd x-axis
            # https://matplotlib.org/examples/axes_grid/parasite_simple2.html
            from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost
            import matplotlib.transforms as mtransforms
            if widget is not None:
                print("False")
                docked = widget.setup_docking("Virtual Annular", "Bottom", figsize=(8.4, 4.8))
                self._f_nav = docked.get_fig()
                self._f_nav.clf()
            else:
                self._f_nav = plt.figure(figsize=(8.4, 4.8))
            ax_nav = SubplotHost(self._f_nav, 1, 2, 1)
            ax_cntrst = SubplotHost(self._f_nav, 1, 2, 2)

            aux_trans = mtransforms.Affine2D().scale(1.0 / mradpp, 1.0)
            ax_mrad = ax_cntrst.twin(aux_trans)
            ax_mrad.set_viewlim_mode("transform")

            self._f_nav.add_subplot(ax_nav)
            self._f_nav.add_subplot(ax_cntrst)

            ax_mrad.axis["top"].set_label('mrad')
            ax_mrad.axis["top"].label.set_visible(True)
            ax_mrad.axis["right"].major_ticklabels.set_visible(False)

        self._f_nav.subplots_adjust(bottom=0.3, wspace=0.3)
        if widget is not None:
            axr1 = fig.add_axes([0.10, 0.05, 0.80, 0.03])
            axr2 = fig.add_axes([0.10, 0.10, 0.80, 0.03])
            axr3 = fig.add_axes([0.10, 0.15, 0.80, 0.03])

        else:
            axr1 = plt.axes([0.10, 0.05, 0.80, 0.03])
            axr2 = plt.axes([0.10, 0.10, 0.80, 0.03])
            axr3 = plt.axes([0.10, 0.15, 0.80, 0.03])

        val_max = self.r_pix.max()
        try:
            self._sr1 = Slider(axr1, 'r1', 0, val_max - 1, valinit=self.r1, valfmt='%0.0f', valstep=1)
            self._sr2 = Slider(axr2, 'r2', 1, val_max, valinit=self.r2, valfmt='%0.0f', valstep=1)
        except AttributeError:
            self._sr1 = Slider(axr1, 'r1', 0, val_max - 1, valinit=self.r1, valfmt='%0.0f')
            self._sr2 = Slider(axr2, 'r2', 1, val_max, valinit=self.r2, valfmt='%0.0f')
        self._sr3 = Slider(axr3, 'rc', 1, val_max, valinit=self.rc, valfmt='%0.1f')

        # these don't seem to work
        #self._sr1.slider_max = self._sr2
        #self._sr2.slider_min = self._sr1

        self._sr1.on_changed(self._update_r_from_slider)
        self._sr2.on_changed(self._update_r_from_slider)
        self._sr3.on_changed(self._update_rc_from_slider)

        ax_nav.imshow(nav_im, norm=norm, cmap=cmap)
        ax_nav.set_xlabel('Detector X (pixels)')
        ax_nav.set_ylabel('Detector Y (pixels)')

        # line plot
        r_cntrst_max = int(np.abs(self.data_shape[-2:] - self.cyx).max())
        dw = 1
        rs = np.arange(dw, r_cntrst_max)

        r1, r2 = self.r1, self.r2
        sls = np.array([self.annular_slice(r - dw, r) for r in rs])
        self.r1, self.r2 = r1, r2

        self._contrast_y = np.std(sls, (1, 2))**2 / np.mean(sls, (1, 2))
        self._contrast_x = rs - dw / 2.0
        ax_cntrst.plot(self._contrast_x, self._contrast_y)
        ax_cntrst.minorticks_on()
        ax_cntrst.set_xlabel('Radius (pixels)')
        ax_cntrst.set_ylabel('Contrast (std^2/mean)')
        self._span = ax_cntrst.axvspan(self.r1, self.r2, color=[1, 0, 0, 0.1], ec='r')

        # wedges
        fc = [0, 0, 0, alpha]
        ec = 'r'
        from matplotlib.patches import Wedge
        self._rmax = val_max + 1
        self._w2 = Wedge(self.cyx[::-1], self._rmax, 0, 360, width=self._rmax - self.r2, fc=fc, ec=ec)
        self._w1 = Wedge(self.cyx[::-1], self.r1, 0, 360, width=self.r1, fc=fc, ec=ec)
        ax_nav.add_artist(self._w2)
        ax_nav.add_artist(self._w1)

        if widget is not None:
            docked = widget.setup_docking("Virtual Annular", "Bottom", figsize=(8.4, 4.8))
            fig = docked.get_fig()
            fig.clf()
            ax_im = fig.subplots(1, 1)
            self._f_im = fig
        else:
            self._f_im, ax_im = plt.subplots(1, 1)
        vmin, vmax = np.percentile(virtual_image, [self._pct, 100 - self._pct])
        self._vim = ax_im.imshow(virtual_image, cmap=cmap, vmin=vmin, vmax=vmax)
        if widget is not None:
            self._cb = fig.colorbar(self._vim)
        else:
            self._cb = plt.colorbar(self._vim)
        self._cb.set_label('Counts')
        ax_im.set_xlabel('Scan X (pixels)')
        ax_im.set_ylabel('Scan Y (pixels)')

        cid = self._f_nav.canvas.mpl_connect('scroll_event', self._onscroll)

        self._sr1.label.set_picker(True)
        self._sr2.label.set_picker(True)
        cid_pick = self._f_nav.canvas.mpl_connect('pick_event', self._onpick)

    def _onpick(self, event):
        if event.artist == self._sr1.label:
            self.r1 = self._sr1.valmin
            self._update_plot_r_from_val()
        if event.artist == self._sr2.label:
            self.r2 = self._sr2.valmax
            self._update_plot_r_from_val()

    def _update_r_from_slider(self, val):
        self.r1 = int(self._sr1.val)
        self.r2 = int(self._sr2.val)
        self.rc = (self.r2 + self.r1) / 2.0

        self._sr3.eventson = False
        self._sr3.set_val(self.rc)
        self._sr3.eventson = True

        _ = self.annular_slice(self.r1, self.r2)

        self._w1.set_radius(self.r1)
        self._w1.set_width(self.r1)
        self._w2.set_width(self._rmax - self.r2)

        xy = self._span.xy
        xy[:, 0] = [self.r1, self.r1, self.r2, self.r2, self.r1]
        self._span.set_xy(xy)

        self._vim.set_data(self.virtual_image)
        #vmin, vmax = self.virtual_image.min(), self.virtual_image.max()
        vmin, vmax = np.percentile(self.virtual_image, [self._pct, 100 - self._pct])
        self._vim.set_clim(vmin, vmax)

        self._f_im.canvas.draw_idle()
        self._f_nav.canvas.draw_idle()

    def _update_rc_from_slider(self, val):
        rc_prev = (self.r2 + self.r1) / 2.0

        drc = self._sr3.val - rc_prev

        self._sr1.eventson = False
        self._sr1.set_val(self._sr1.val + drc)
        self._sr1.eventson = True

        self._sr2.eventson = False
        self._sr2.set_val(self._sr2.val + drc)
        self._sr2.eventson = True

        self._update_r_from_slider(None)

    def _update_plot_r_from_val(self):
        self._sr1.eventson = False
        self._sr1.set_val(self.r1)
        self._sr1.eventson = True

        self._sr2.eventson = False
        self._sr2.set_val(self.r2)
        self._sr2.eventson = True

        self._update_r_from_slider(None)

    def _onscroll(self, event):
        if event.inaxes not in [self._sr1.ax, self._sr2.ax, self._sr3.ax]:
            return
        if event.button == 'up':
            dr = self._scroll_step
        else:
            dr = -self._scroll_step

        if event.inaxes == self._sr1.ax:
            self.r1 += dr
        elif event.inaxes == self._sr2.ax:
            self.r2 += dr
        else:
            self.r1 += dr
            self.r2 += dr
        self._update_plot_r_from_val()
