from __future__ import print_function

'''
'''


# file module version (separate from fpd version)
__version__ = '0.1.1'
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import griddata
import sys
from itertools import product
from collections import namedtuple
from tqdm import tqdm
import io
from pkg_resources import parse_version
import logging
from distutils.version import LooseVersion
import matplotlib as mpl
import matplotlib.pyplot as plt
import inspect
from functools import partial
import os
from collections import MutableMapping
import re
import codecs
from dateutil.parser import parse
import time
from collections import OrderedDict
import numpy as np
import h5py
import mmap
_min_version = '0.1.0'

#from . import _p3
# python version
_p3 = False
if sys.version_info > (3, 0):
    _p3 = True


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
#_handler.setFormatter(logging.Formatter(fmt='%(levelname)s:%(name)s:%(message)s'))
_handler.setFormatter(logging.Formatter(fmt='%(levelname)s: %(message)s'))
_logger.addHandler(_handler)


if _p3:
    _str_type_list = [str]
    _input_fn = input
else:
    _str_type_list = [str, unicode]
    _input_fn = raw_input


_mpl_non_adjust = False
_mplv = mpl.__version__
if LooseVersion(_mplv) >= LooseVersion('2.2.0'):
    _mpl_non_adjust = True



class DataBrowserNew:
    def __init__(self, fpgn, nav_im=None, cmap=None, colour_index=None,
                 nav_im_dict=None, fpd_check=True, fig_1 = None, fig_2 = None):
        '''
        Navigate fpd data set.
        
        Parameters
        ----------
        fpgn : hdf5 str, file, group, dataset, ndarray, or dask array.
             hdf5 filename, file, group or dataset, or numpy array, 
             `MerlinBinary` object, or dask array.
        nav_im : 2-D array or None
            Navigation image. If None, this is taken as the sum image.
            For numpy arrays, it is calculated directly.
        cmap : str or None
            Matplotlib colourmap name used for diffraction image.
            If None, `viridis` is used if available, else `gray`.
        colour_index : int or None
            Colour index used for plotting. If None, the first index is
            used.
        nav_im_dict : None or dictionary
            Keyword arguments passed to the navigation imshow call.
        fpd_check : bool
            If True, the file format version is checked.

        TODO
        ----
        log / linear norms
        nav_im list input and switch between images?
        display with axis units rather than pixels?
            
        '''

        import fpd
        self.fig_1 = fig_1
        self.fig_2 = fig_2
        numpy_array = isinstance(fpgn, np.ndarray) or isinstance(
            fpgn, fpd.fpd_file.MerlinBinary)
        dask_array = "dask.array.core.Array" in str(type(fpgn))
        if not numpy_array and not dask_array:
            if fpd_check:
                b, vs = _check_fpd_file(fpgn)
                if not b:
                    raise Exception('Not a valid FPD file. Version:', vs)

            try:
                # try to use FPD hdf5 format
                self.closef, self.h5f = _get_hdf5_file_from_obj(fpgn)
                self.h5f_ds = self.h5f['fpd_expt/fpd_data/data']
            except:
                self.closef = False
                self.h5f_ds = fpgn
        elif numpy_array:
            # numpy array
            self.closef = False
            self.h5f_ds = fpgn
        elif dask_array:
            self.closef = False
            self.h5f_ds = fpgn

        self.nav_im_dict = nav_im_dict

        # get data shape info
        self.scanY, self.scanX = self.h5f_ds.shape[:2]
        self.detY, self.detX = self.h5f_ds.shape[-2:]

        # determine colour info
        ds_shape_len = len(self.h5f_ds.shape)
        if ds_shape_len == 4:
            # no colour data
            self.ncolours = 0
        elif ds_shape_len == 5:
            self.ncolours = self.h5f_ds.shape[2]

        self.colour_index = None
        if colour_index is None and self.ncolours:
            self.colour_index = 0

        # navigation image
        if nav_im is None and not numpy_array:
            if self.colour_index is not None:
                self.nav_im = self.h5f['fpd_expt/fpd_sum_im/data'].value[...,
                                                                         self.colour_index]
            else:
                self.nav_im = self.h5f['fpd_expt/fpd_sum_im/data'].value[...]
        else:
            self.nav_im = nav_im
        if self.nav_im is None:
            # numpy array
            if self.ncolours == 0:
                self.nav_im = self.h5f_ds.sum((-2, -1))
            else:
                self.nav_im = self.h5f_ds[:, :,
                                          self.colour_index].sum((-2, -1))

        self.scanYind = 0
        self.scanXind = 0
        self.scanYind_old = self.scanYind
        self.scanXind_old = self.scanXind
        if self.colour_index is not None:
            self.plot_data = self.h5f_ds[self.scanYind,
                                         self.scanXind, self.colour_index, :, :]
        else:
            self.plot_data = self.h5f_ds[self.scanYind, self.scanXind, :, :]
        self.plot_data = np.ascontiguousarray(self.plot_data)

        self.rwh = max(self.scanY, self.scanX)//64
        if self.rwh == 0:
            self.rwh = 2
        self.rect = None
        self.press = None
        self.background = None
        self.plot_nav_im()

        # cmap
        if cmap is None:
            try:
                self.cmap = mpl.cm.get_cmap('viridis')
            except ValueError:
                self.cmap = mpl.cm.get_cmap('gray')
        else:
            self.cmap = mpl.cm.get_cmap(cmap)
        self.cmap.set_bad(self.cmap(0))

        self.plot_dif()
        self.connect()

    def plot_nav_im(self):
        kwd = dict(adjustable='box-forced', aspect='equal')
        if _mpl_non_adjust:
            _ = kwd.pop('adjustable')
        if self.fig_1:
            plt = self.fig_1            
            ax = plt.subplots(subplot_kw=kwd)
            self.f_nav = plt.canvas
        else:
            self.f_nav, ax = plt.subplots(subplot_kw=kwd)
            self.f_nav.canvas.set_window_title('nav')


        d = {'cmap': 'gray'}
        if self.nav_im_dict is not None:
            d.update(self.nav_im_dict)
        im = ax.imshow(self.nav_im, interpolation='nearest', **d)
        if self.nav_im.ndim != 3:
            plt.colorbar(mappable=im)

        rect_c = 'r'
        if self.nav_im.ndim == 3 or (self.nav_im.ndim == 2 and im.cmap.name != 'gray'):
            # rgb
            rect_c = 'w'  # 'k'
        self.rect = mpl.patches.Rectangle((self.scanYind-self.rwh/2,
                                           self.scanXind-self.rwh/2),
                                          self.rwh, self.rwh, ec=rect_c,
                                          fc='none', lw=2, picker=4)
        ax.add_patch(self.rect)
        plt.tight_layout()
        #plt.draw()

    def plot_dif(self):
        kwd = dict(adjustable='box-forced', aspect='equal')
        if _mpl_non_adjust:
            _ = kwd.pop('adjustable')
        if self.fig_2:
            plt = self.fig_2
            ax = plt.subplots(subplot_kw=kwd)
            self.f_dif = plt.canvas
        else:
            self.f_dif, ax = plt.subplots(subplot_kw=kwd)
            self.f_dif.canvas.set_window_title('dif')

        if self.plot_data.max() < 1:
            norm = None
        else:
            norm = mpl.colors.LogNorm()
        self.im = ax.matshow(self.plot_data,
                             interpolation='nearest',
                             cmap=self.cmap,
                             norm=norm)
        plt.sca(ax)
        self.cbar = plt.colorbar(self.im)
        ax.format_coord = self.format_coord
        self.update_dif_plot()

        plt.tight_layout()
        #plt.draw()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

        # self.cid_f_nav = self.f_nav.canvas.mpl_connect(
        #     'close_event', self.handle_close)
        # self.cid_f_dif = self.f_dif.canvas.mpl_connect(
        #     'close_event', self.handle_close)

    def handle_close(self, e):
        if self.closef == True:
            self.h5f.file.close()
        self.disconnect()
        # close other fig
        if e.canvas.get_window_title() == 'nav':
            plt.close(self.f_dif)
        else:
            plt.close(self.f_nav)

    def on_press(self, event):
        if event.inaxes != self.rect.axes:
            return

        contains, attrd = self.rect.contains(event)
        if contains:
            #print('event contains', self.rect.xy)
            x0, y0 = self.rect.xy   # xy is lower left

            # draw everything but the selected rectangle and store the pixel buffer
            canvas = self.rect.figure.canvas
            axes = self.rect.axes
            self.rect.set_animated(True)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

            axes.draw_artist(self.rect)     # now redraw just the rectangle
            canvas.blit(axes.bbox)          # and blit just the redrawn area
        else:
            # in axis but not rectangle
            #print event.xdata, event.ydata
            x0, y0 = (None,)*2

        self.press = x0, y0, event.xdata, event.ydata
        self.yind_temp = self.scanYind
        self.xind_temp = self.scanXind

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.rect.axes:
            return
        if self.background is None:
            return

        x0, y0, xpress, ypress = self.press
        dx = int(event.xdata - xpress)
        dy = int(event.ydata - ypress)
        if abs(dy) > 0 or abs(dx) > 0:
            #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f'%(x0, xpress, event.xdata, dx, x0+dx))
            self.rect.set_x(x0+dx)
            self.rect.set_y(y0+dy)
            self.scanYind = self.yind_temp+dy
            self.scanXind = self.xind_temp+dx
            #print(dy, dx)

            canvas = self.rect.figure.canvas
            axes = self.rect.axes
            # restore the background region
            canvas.restore_region(self.background)
            # redraw just the current rectangle
            axes.draw_artist(self.rect)
            # blit just the redrawn area
            canvas.blit(axes.bbox)

            #self.rect.figure.canvas.draw()
            self.update_dif_plot()

    def on_release(self, event):
        if event.inaxes != self.rect.axes:
            return

        x, y = self.press[2:]
        if np.round(event.xdata-x) == 0 and np.round(event.ydata-y) == 0:
            # mouse didn't move
            x, y = np.round(x), np.round(y)
            self.rect.set_x(x-self.rwh/2)
            self.rect.set_y(y-self.rwh/2)
            self.scanYind = int(y)
            self.scanXind = int(x)

            #self.rect.figure.canvas.draw()
            self.update_dif_plot()
        elif self.background is not None:
            canvas = self.rect.figure.canvas
            axes = self.rect.axes
            # restore the background region
            canvas.restore_region(self.background)
            # redraw just the current rectangle
            axes.draw_artist(self.rect)
            # blit just the redrawn area
            canvas.blit(axes.bbox)

        'on release we reset the press data'
        self.press = None
        self.yind_temp = None
        self.yind_temp = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()

    def format_coord(self, x, y):
        col = np.ceil(x-0.5).astype(int)
        row = np.ceil(y-0.5).astype(int)
        if col >= 0 and col < self.detX and row >= 0 and row < self.detY:
            z = self.plot_data[row, col]
            return 'x=%d, y=%d, z=%d' % (x, y, z)
        else:
            return 'x=%d, y=%d' % (x, y)

    def update_dif_plot(self):
        if self.colour_index is not None:
            self.plot_data = self.h5f_ds[self.scanYind,
                                         self.scanXind, self.colour_index, :, :]
        else:
            self.plot_data = self.h5f_ds[self.scanYind, self.scanXind, :, :]
        self.plot_data = np.ascontiguousarray(self.plot_data)
        self.im.set_data(self.plot_data)
        self.im.autoscale()
        self.im.changed()
        self.im.axes.set_xlabel('scanX %s' % self.scanXind)
        self.im.axes.set_ylabel('scanY %s' % self.scanYind)
        self.im.axes.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

        # self.f_nav.canvas.mpl_disconnect(self.cid_f_nav)
        # self.f_dif.canvas.mpl_disconnect(self.cid_f_dif)
