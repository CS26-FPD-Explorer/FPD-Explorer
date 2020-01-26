from distutils.version import LooseVersion

import datetime
import numpy as np
import scipy as sp
from scipy import ndimage
import collections
import os
import numbers
import json

import matplotlib as mpl
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import Slider
from matplotlib.widgets import RadioButtons
import matplotlib.pylab as plt

from fpd.gwy import writeGSF
from fpd.ransac_tools import ransac_im_fit
from fpd import _p3
from fpd.utils import median_of_difference_lc, median_lc

try:
    from fpd_explorer import config_handler as config
    dark_mode = config.get_config("dark_mode")
    print("sucessful imprt")
except ImportError:
    dark_mode = False


#from fpd_explorer.dpc_explorer import DPC_Explorer_Widget
mplv2 = int(plt.matplotlib.__version__.split('.')[0]) >= 2


_mpl_non_adjust = False
_mplv = mpl.__version__
if LooseVersion(_mplv) >= LooseVersion('2.2.0'):
    _mpl_non_adjust = True


# disable forward and reverse views with arrow keys
try:
    mpl.rcParams['keymap.back'].remove('left')
    mpl.rcParams['keymap.forward'].remove('right')
except:
    pass


class DPC_Explorer:
    def __init__(self, d, r_min=0, r_max=None, r_min_pct=0, r_max_pct=95,
                 descan=[0, 0, 0, 0], cyx=None, vectrot=0, gaus=0, pct=None,
                 dt=0, gaus_lim=16, cw_rmin=1.0/3, cmap=None, median=False,
                 median_mode=0, ransac=False, ransac_dict=None, nbins=None,
                 hist_lims=None, flip_y=False, flip_x=False, origin='top',
                 yx_range_from_r=True, widget = None):
        '''
        Interactive plots of vector field using matplotlib.
        
        Returns class from which the save method can be used to 
        programmatically save the analysis.
        
        Parameters
        ----------
        d : array-like or int
            If array-like, yx data. If length 2 iterable or ndarray of
            shape (2, M, N), data is single yx dataset. If shape is 
            (S, 2, M, N), a sequence yx data of length S can be plotted.
            If int, width of array of synthetic data.
            If int is negative, synthetic data has noise added.
        r_min : scalar
            Initial value of `r_min`.
            If supplied, takes precedence over `r_min_pct`.
        r_max : scalar
            Initial value of `r_max`.
            If supplied, takes precedence over `r_max_pct`.
        r_min_pct : scalar
            [0 100] used for initial setting of `r_min`.
        r_max_pct : scalar
            [0 100] used for initial setting of `r_max`.
        descan : length 4 iterable
            Plane descan correction.
            [Yy, Yx, Xy, Xx] entered in 1/1000 for for convenience.
        cyx : length 2 iterable
            y, x centre coordinates.
        vectrot : scalar
            Rotation of data vector (not CW) in degrees.
        gaus : scalar
            Sigma of Gaussian smoothing used on yx data.
        pct : None, scalar or iterable
            Percentile used to apply to separately to x and y.
            If None, no percentile.
            If scalar, used for all values.
            If iterable, used as [y, x], then [[ylow, yhigh], [ylow, yhigh]].
        dt : scalar
            Rotation of colourwheel (not data) in degrees.
        gaus_lim : scalar
            Sets max scale on gaus sigma slider.
        cw_rmin : scalar
            Inner radius of colourwheel, [0:1].
        cmap : mpl.colors.Colormap, string, or integer
            Colour map for r-theta plot.
            If string, must be name of matplotlib.Colormap.
            If integer, selects n'th built-in cmaps. 
        median : bool
            If True, apply median line correction to data vertically.
            This assumes scan is sequence of horizontal lines.
        median_mode : int
            Median line correction mode. 
            0 : median
            1 : median of differences
        ransac : bool
            If True, ransac background subtraction is applied to x and y data.
            This is computationally expensive and so is only run once, then
            stored for reuse, unless GUI button is toggled.
        ransac_dict : dictionary or None
            Ransac parameter dictionary passed as keyword dict to ransac function.
            See fpd.ransac_tools.ransac_im_fit for details of parameters.
            If None, plane background is used.
        nbins : int or None
            Number of bins to use for histogram.
            If None, the number of bins is calculated from the data size.
            The bin widths are always equal in x and y.
        hist_lims : length 4 tuple of scalars, or None
            Histogram limits in order of xmin, xmax, ymin, ymax.
            If None, limits are taken from data.
        flip_y : bool
            If True, flip y beam shifts.
        flip_x : bool
            If True, flip x beam shifts.
        origin : str
            Controls y-origin of supplied shift arrays. If origin='top', pythonic
            indexing is used. If origin='bottom', increasing y is up.
        yx_range_from_r : bool
            If True, the y and x plot ranges are set from the maximum radius. The
            centre is always set from the centre.
        widgte : DPC_Explorer_Widget
            A qt widget that must contain either 4 widget or 4 dock widgets.

        Attributes
        ----------
        x : 2-D array
            Processed x values.
        y : 2-D array
            Processed y values.
        r : 2-D array
            Radius values.
        rn : 2-D array
            Radius values, normalised and clipped at `r_max`, in [0, 1].
        tn : 2-D array
            Theta values in radians, in range [0, 2pi].
        t_im : 3-D array
            Theta RGB float [0, 1] image of shape (..., 3).
        tr_im : 3-D array
            Magnitude scaled theta RGB float [0, 1] image of shape (..., 3).
            
        Notes
        -----        
        On histogram:
            right / left arrows for sequence navigation.
            Ctrl+arrows for Y descan.
            Alt+arrows for X descan.
            Increment is fraction of r_max.
            
            Ctrl+ mouse drag on circle is rotate angle.
            Mouse drag on circle sets r_max.
            Shift+ mouse drag on circle sets r_min.
            Mouse drag on square moves centre.
            
        On xy plots:
            Click+drag in y for histogram region select.
        
        Order of process operations:
            1. median
            2. ransac background
            3. manual descan
            4. flip displacements
            5. percentile
            6. gaussian smoothing
            7. vector rotation
        
        Descan correction happens early so that manual or programmatic 
        correction can be used without affecting other parameters.
              
        The histogram is generated from processed x-y data.
        
        The x and y data are plotted relative to chosen centre on histogram 
        with same range on each so relative magnitudes can easily be seen.
        
        Examples
        --------
        A noiseless plot:
        
        >>> import matplotlib.pylab as plt
        >>> plt.ion()
        >>> import fpd
        >>> b = fpd.DPC_Explorer(64)
        >>> save_dir = b.save('Test')     
        
        A plot with random noise:
        
        >>> ransac_dict = {'mode': 1, 'residual_threshold': 0.1}
        >>> b = fpd.DPC_Explorer(-64, ransac=True, ransac_dict=ransac_dict)
        
        A sequence of 3 datasets:
        
        >>> import matplotlib.pylab as plt
        >>> import fpd
        >>> import numpy as np
        >>> plt.ion()
        >>> yx = np.random.rand(3, 2, 64, 64)
        >>> yx -= yx.mean((2,3))[..., None, None]
        >>> yx[-2,0] += 0.5
        >>> yx[-1,0] += 1.0
        >>> b = fpd.DPC_Explorer(d=yx)
        
        
        TODO
        ----
        Reset hist regions / plot limits on updates?
            
        Avoid rare issues of small radii by updating rwh size or
        by making centre click move circle, not rectangle drag?
            
        '''

        self.widget = widget
        plt.ion()

        create_time = datetime.datetime.now()
        self._create_time = create_time.strftime("%Y%m%d_%H%M%S")

        self._figs = []

        self._origin = origin.lower()
        if isinstance(d, int):
            dim = np.indices((np.abs(d),)*2).astype(float)
            dim -= dim.mean((1, 2))[:, None, None]
            dim *= np.array([-1, 1])[:, None, None]      # flip y
            if d < 0:
                dim += np.random.rand(*dim.shape)*10
            d = dim
        else:
            d = np.array(d)
            # default origin implementation is bottom
            if self._origin == 'top':
                d[..., 0, :, :] *= -1

        if d.ndim == 4:
            # sequence
            self._seq = True
            self._seq_data = d
            self._seq_length = len(self._seq_data)
            self._seq_ind = 0
            self.y, self.x = self._seq_data[self._seq_ind]
        else:
            self._seq = False
            self.y, self.x = d          # data of order (yx, Y, X)

        self._vectrot = vectrot
        self._gaus = gaus
        self._gaus_lim = gaus_lim
        self._cw_rmin = cw_rmin
        self._median = median
        self._median_mode = median_mode
        self._ransac_dict = ransac_dict
        self._ransac = ransac

        if median_mode not in [0, 1]:
            raise NotImplementedError("'median_mode' must be in [0, 1]")

        self._nbins = nbins
        self._hist_lims = hist_lims

        self._flip_y = flip_y
        self._flip_x = flip_x

        if self._ransac_dict is None:
            self._ransac_dict = {'mode': 1, 'scale': True, 'fract': 0.5}

        if isinstance(pct, (int, float)):
            self._pct = ((pct,)*2,)*2
        elif isinstance(pct, (collections.Sequence, np.ndarray)):
            y_pct = pct[0]
            x_pct = pct[1]
            if isinstance(y_pct, (int, float)):
                y_pct = (pct,)*2
            if isinstance(x_pct, (int, float)):
                x_pct = (pct,)*2
            self._pct = (y_pct, x_pct)
        else:
            self._pct = ((0,)*2,)*2

        descan = [ds/1000.0 for ds in descan]
        self._descanY_factY, self._descanY_factX, self._descanX_factY, self._descanX_factX = descan
        self._y_orig, self._x_orig = self.y.copy(), self.x.copy()
        self._make_scan_indices()
        self._calc_data(calc_ransac=self._ransac)

        if cyx is None:
            self._yc, self._xc = self.y.mean(), self.x.mean()
        else:
            self._yc, self._xc = cyx
        self._yc_orig, self._xc_orig = self._yc, self._xc
        print('Mean centre (y,x): %0.4f, %0.4f' % (self._yc, self._xc))

        self._circ_r_max = None
        self._circ_r_min = None
        self._rect = None
        self._press = None           # holds data about press
        self._press_cnt = False      # logic for press in centre (rect)

        self._tmp_fns = []
        self._xy_ims = None

        # CMAP
        self._init_cmap(cmap)

        # radius theta
        self.r = None
        self._t = None

        self._r_max = r_max
        self._r_min = r_min
        if r_max is not None:
            r_max_pct = None
        if r_min is not None:
            r_min_pct = None
        # commented out so inverse plots can be made
        #if r_min is not None and r_max is not None:
            #if r_min >= r_max:
            #r_min = 0
        self._hist_title = None
        self.rn = None      # [0 1] normalised with possible clipping
        self.tn = None          # [0 1] normalised
        self.t_im = None        # theta image array
        self.tr_im = None       # theta(r) image array
        self._t_ims = None       # theta image arrays [rgb, r_value]
        self._im_objs = None     # r t image objects

        self._ctrl = False       # for mouse rotate
        self._shift = False      # for mouse r_min
        self._dt = np.deg2rad(dt)
        self._dt_orig = self._dt
        self._calc_rt(r_max_pct, r_min_pct)

        self._yx_range_from_r = yx_range_from_r
        self._plot_xy()

        self._plot_hist()
        self._plot_rt()

        self._cw_im_objs = None
        self._plot_cw()

        #self._figs[1].canvas.manager.window.raise_()
        #'''
        try:
            self._figs[1].canvas.manager.window.raise_()
        except AttributeError as e:
            # probably in an ipython notebook
            pass
        #'''
        self._connect()

    # scanY, scanX
    def _make_scan_indices(self):
        self._inds = np.indices(self._y_orig.shape).astype(float)
        self._inds -= self._inds.mean((1, 2))[:, None, None]       # centered

    def _init_cmap(self, cmap_in):
        self._cmaps = collections.OrderedDict()     # dict of all cmaps

        # user supplied
        if cmap_in is not None and not isinstance(cmap_in, numbers.Integral):
            if isinstance(cmap_in, str):
                cmap_in = mpl.cm.get_cmap(cmap_in)
            elif isinstance(cmap_in, mpl.colors.Colormap):
                cmap_in = cmap_in
            else:
                raise Exception('cmap not understood')
            self._cmaps['my_cmap'] = cmap_in

        # modified hsv
        theta = np.linspace(0, np.pi*2, 256)
        r = np.cos((theta))
        g = np.cos((theta-np.pi*2/3))
        b = np.cos((theta-np.pi*4/3))
        r, g, b = [(x+1)/2 for x in (r, g, b)]
        rgb = np.vstack([r, g, b]).T                # Nx3
        hsv_mod = mpl.colors.ListedColormap(rgb)
        self._cmaps['HSV_mod'] = hsv_mod

        #hsv
        self._cmaps['HSV'] = mpl.cm.get_cmap('hsv')

        # rygb
        clr_array = np.array([(1, 0, 0), (1, 0.65, 0), (1, 1, 0), (0.6, 1, 0),
                              (0, 1, 0), (0, 0.6, 0.6), (0.15, 0.15, 1),
                              (0.5, 0, 0.5)])
        theta = np.arange(360)
        thetap = np.linspace(0, 360, clr_array.shape[0], endpoint=False)
        clr_interp = [np.interp(theta, thetap, clr_array[:, i], period=360)
                      for i in range(3)]
        clr_interp = np.array(clr_interp).T
        rygb_cmap = mpl.colors.ListedColormap(clr_interp)

        '''
        # plot
        f, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)
        cs = ['r', 'g', 'b']
        [ax1.plot(theta, clr, c) for (clr, c) in zip(clr_interp.T, cs)]
        ax1.margins(y=0.1)

        d = np.tile(clr_interp[None,...], (100,1,1))
        ax2.imshow(d)
        ax2.set_aspect('auto')

        d2 = clr_interp[None,...] * np.linspace(0, 1, 100+1)[::-1,None, None]
        ax3.imshow(d2)
        '''
        self._cmaps['RYGB'] = rygb_cmap

        # perceptually uniform
        fn = 'perceptually_uniform_cmap.npy'
        try:
            rgb = np.load(os.path.join(os.path.split(__file__)[0], fn))
            mycmap = mpl.colors.ListedColormap(rgb)
            self._cmaps['MLP'] = mycmap
        except IOError as e:
            print("WARNING: Perceptually uniform cmap MPL not found.")
            pass

        # set current cmap
        if isinstance(cmap_in, numbers.Integral):
            # to cmapth entry
            pass
        else:
            # to first entry
            cmap_in = 0
        self._cmap_curent = list(self._cmaps.items())[cmap_in]  # (cmap_name, cmap)

    def _calc_data(self, calc_ransac=False):
        # median
        if self._median:
            if self._median_mode == 0:
                mf = median_lc
            if self._median_mode == 1:
                mf = median_of_difference_lc
            self.x = mf(self._x_orig, 1)
            self.y = mf(self._y_orig, 1)
        else:
            self.x = self._x_orig.copy()
            self.y = self._y_orig.copy()

        # ransac
        if self._ransac:
            if calc_ransac:
                self._fitx, _, _ = ransac_im_fit(self.x, **self._ransac_dict)
                self._fity, _, _ = ransac_im_fit(self.y, **self._ransac_dict)
            self.x -= self._fitx
            self.y -= self._fity

        # descan
        self._descany = (self._inds[0]*self._descanY_factY
                         + self._inds[1]*self._descanY_factX)
        self._descanx = (self._inds[0]*self._descanX_factY
                         + self._inds[1]*self._descanX_factX)

        self.y = self.y + self._descany
        self.x = self.x + self._descanx

        # flip
        if self._flip_y:
            y_centre = np.percentile(self.y, 50)
            self.y = 2.0*y_centre - self.y

        if self._flip_x:
            x_centre = np.percentile(self.x, 50)
            self.x = 2.0*x_centre - self.x

        # percentile
        if self._pct:
            ymin, ymax = np.percentile(self.y,
                                       [self._pct[0][0], 100-self._pct[0][1]])
            self.y = self.y.clip(ymin, ymax)
            xmin, xmax = np.percentile(self.x,
                                       [self._pct[1][0], 100-self._pct[1][1]])
            self.x = self.x.clip(xmin, xmax)

        # Gaussian smoothing
        self.x = sp.ndimage.gaussian_filter(self.x, sigma=self._gaus)
        self.y = sp.ndimage.gaussian_filter(self.y, sigma=self._gaus)

        # vector rotation
        def rotvec(y, x, deg):
            # rotate vector anticlockwise by angle deg (>0)
            r = np.sqrt(y**2 + x**2)
            t = np.arctan2(y, x)
            t2 = t+np.deg2rad(deg)
            y2 = r*np.sin(t2)
            x2 = r*np.cos(t2)
            return y2, x2
        self.y, self.x = rotvec(self.y, self.x, self._vectrot)

    def _plot_xy(self):
        kwd = dict(adjustable='box-forced', aspect='equal')
        if _mpl_non_adjust:
            _ = kwd.pop('adjustable')

        window_name = 'xy'
        if self.widget is not None:
            docked = self.widget.setup_docking(window_name)
            self.fig = docked.get_fig()
            self.fig.clf()
        
            (ax1, ax2) = self.fig.subplots(1, 2, True, True,subplot_kw=kwd)
            f = self.fig.canvas
        else:
            f, (ax1, ax2) = plt.subplots(1, 2, True, True,
                                figsize=(6.4, 4),
                                subplot_kw=kwd)

            f.canvas.set_window_title(window_title)
            self.fig = plt

        ims = []
        self._figs.append(f)

        y, x = self.y-self._yc, self.x-self._xc
        if self._yx_range_from_r:
            vmin, vmax = -self._r_max, self._r_max
        else:
            vmin, vmax = np.percentile(np.column_stack([y, x]), [0, 100])

        for ax, d, t in zip((ax1, ax2), [y, x], ['y', 'x']):
            im = ax.imshow(d,
                           interpolation='nearest',
                           cmap='gray',
                           vmin=vmin,
                           vmax=vmax)
            ax.set_title(t+' stdev: %0.3e' % (d.std()))
            ax.set_axis_off()
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ims.append(im)
        self._xy_ims = ims
        self.fig.tight_layout()

        ## open in Gwyddion
        self.fig.subplots_adjust(bottom=0.1)
        # open Y
        axGY = self.add_axes([0.02, 0.02, 0.10, 0.05])
        self._bGY = mpl.widgets.Button(axGY, 'Open Y')
        self._bGY.on_clicked(self._on_GY)
        # open X
        axGX = self.add_axes([0.14, 0.02, 0.10, 0.05])
        self._bGX = mpl.widgets.Button(axGX, 'Open X')
        self._bGX.on_clicked(self._on_GX)

        axYXr = self.add_axes([0.26, 0.02, 0.10, 0.05])
        self._bYXr = mpl.widgets.Button(axYXr, 'lim <- r')
        self._bYXr.on_clicked(self._on_YXr)
        if self._yx_range_from_r:
            if mplv2:
                self._bYXr.ax.set_facecolor('green')
            else:
                self._bYXr.ax.set_axis_bgcolor('green')

        if self.widget is None:
            plt.draw()
        else:
            docked.get_canvas().draw()

        # rectangle selector for histogram only, not using middle button
        self._xy_selector = RectangleSelector(ax1,
                                              self._xy_select_callback,
                                              drawtype='box',
                                              useblit=False,
                                              button=[1, 3],
                                              minspanx=5,
                                              minspany=5,
                                              spancoords='pixels',
                                              interactive=True)

        if self.widget is None:
            f.canvas.mpl_connect('key_press_event', self._on_xy_plot_key)
            f.canvas.mpl_connect(self._xy_selector.onmove, self._update_hist_plot)

        else:
            docked.get_canvas().mpl_connect('key_press_event', self._on_xy_plot_key)
            docked.get_canvas().mpl_connect(self._xy_selector.onmove, self._update_hist_plot)



    def _on_YXr(self, event):
        self._yx_range_from_r = not self._yx_range_from_r
        if self._yx_range_from_r:
            if mplv2:
                self._bYXr.ax.set_facecolor('green')
            else:
                self._bYXr.ax.set_axis_bgcolor('green')
        self._update_xy_plot()

    def _on_GY(self, event):
        sy, sx = self.y.shape
        filename = writeGSF(filename=None,
                            data=self.y,
                            XReal=1.0*sx,
                            YReal=1.0*sy,
                            Title='Y',
                            open_file=True)
        self._tmp_fns.append(filename)
        print("Wrote Y to '%s'." % (filename))

    def _on_GX(self, event):
        sy, sx = self.x.shape
        filename = writeGSF(filename=None,
                            data=self.x,
                            XReal=1.0*sx,
                            YReal=1.0*sy,
                            Title='Y',
                            open_file=True)
        self._tmp_fns.append(filename)
        print("Wrote X to '%s'." % (filename))

    def _xy_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print(" buttons: %s %s" % (eclick.button, erelease.button))
        self._update_hist_plot()

    # to reshow selector
    #b.xy_selector.update()
    # to check visible
    #b.xy_selector.artists[0].get_visible()

    def _on_xy_plot_key(self, event):
        # to reset hist on cleared selection
        if event.key == 'escape':
            self._update_hist_plot()

    def _update_xy_plot(self):
        #y, x = self.y, self.x
        y, x = self.y-self._yc, self.x-self._xc
        if self._yx_range_from_r:
            vmin, vmax = -self._r_max, self._r_max
        else:
            vmin, vmax = np.percentile(np.column_stack([y, x]), [0, 100])

        for im, imd, t in zip(self._xy_ims, [y, x], ['y', 'x']):
            im.set_data(imd)
            #im.autoscale()
            im.set_clim((vmin, vmax))
            im.axes.title.set_text(t+' stdev: %0.3e' % (imd.std()))
        im.figure.canvas.draw_idle()

        # to reshow on draw
        if self._xy_selector.artists[0].get_visible():
            self._xy_selector.update()

    def _calc_rt(self, r_max_pct=None, r_min_pct=None):
        cy = self.y-self._yc
        cx = self.x-self._xc

        self.r = np.sqrt(cy**2 + cx**2)
        self._t = np.arctan2(cy, cx)
        # applied angle offset to plot data
        tplot = self._t-self._dt
        self._t[self._t < 0] += 2*np.pi
        self._t[self._t > 2*np.pi] -= 2*np.pi
        tplot[tplot < 0] += 2*np.pi
        tplot[tplot > 2*np.pi] -= 2*np.pi

        # create hsv theta array
        self.tn = self._t/(2*np.pi)
        # angle offset applied
        t_rgba = self._cmap_curent[1](tplot/(2*np.pi))

        # calculate normalised r
        if r_min_pct is not None:
            # first call
            self._r_min = np.percentile(self.r, r_min_pct)
        if r_max_pct is not None:
            self._r_max = np.percentile(self.r, r_max_pct)
        else:
            # all other calls use r_max, r_min
            #r_min = 0   # self._r_max
            pass
        # Could check r_min < r_max, but allowed so inversion of values
        # will plot removed regions.
        self.rn = (self.r-self._r_min)/(self._r_max-self._r_min)
        self.rn = self.rn.clip(0, 1)

        ## create rgb theta with different scalling by r
        #t_hsv = mpl.cm.colors.rgb_to_hsv(t_rgba[...,:3])
        #t_hsv_v = t_hsv.copy()
        #t_hsv_v[...,2]*=self.rn
        #t_rgb_v = mpl.cm.colors.hsv_to_rgb(t_hsv_v)

        t_rgb_v = t_rgba*self.rn[..., None]
        self.t_im = t_rgba[:, :, :3]
        self.tr_im = t_rgb_v[:, :, :3]
        self._t_ims = [self.t_im, self.tr_im]

    def _hist_tit_str(self):
        tit = '(cy, cx), (r_min, r_max): (%0.3f, %0.3f), (%0.3f, %0.3f)    dt: %0.3f\nDescan Y(y,x), X(y,x) x1000: (%0.3f, %0.3f), (%0.3f, %0.3f)\n' % (self._yc, self._xc, self._r_min, self._r_max, self._dt/np.pi*180,
                                                                                                                                                        self._descanY_factY*1000, self._descanY_factX*1000,
                                                                                                                                                        self._descanX_factY*1000, self._descanX_factX*1000)
        return tit

    def _update_calcs_and_plots(self, calc_ransac=False):
        self._calc_data(calc_ransac=calc_ransac)
        self._update_xy_plot()
        self._update_hist_plot()
        self._calc_rt()
        self._update_rt_plot()

    def _update_gaus(self, val):
        self._gaus = val
        self._update_calcs_and_plots()

    def _update_vectrot(self, val):
        self._vectrot = val
        self._update_calcs_and_plots()

    def _plot_hist(self):
        window_name = 'hist'

        if self.widget is not None:
            docked = self.widget.setup_docking(window_name)
            self.fig = docked.get_fig()
            self.fig.clf()

            ax = self.fig.subplots()
            f = self.fig.canvas
        else:
            f, ax = plt.subplots()
            f.canvas.set_window_title(window_name)
            self.fig = plt

        self.fig.subplots_adjust(bottom=0.27, left=0.2)
        ax.set_aspect(1)
        plt.minorticks_on()
        self._figs.append(f)

        if self._nbins is None:
            self._nbins = int(np.prod(self.x.size)**0.5/2)
        if self._hist_lims is None:
            if self._seq:
                ys = self._seq_data[:, 0]
                xs = self._seq_data[:, 1]
            else:
                ys = self.y
                xs = self.x

            # pct is currently fixed at instantiation, so hist limits can be clipped
            ymin, ymax = np.percentile(ys,
                                       [self._pct[0][0], 100-self._pct[0][1]])
            xmin, xmax = np.percentile(xs,
                                       [self._pct[1][0], 100-self._pct[1][1]])
            #xmin, xmax = xs.min(), xs.max()
            #ymin, ymax = ys.min(), ys.max()
        else:
            xmin, xmax, ymin, ymax = self._hist_lims
        rng = np.max([xmax-xmin, ymax-ymin])/2.0
        xc = (xmin + xmax)/2.0
        yc = (ymin + ymax)/2.0
        xy_bins = [np.linspace(xc-rng, xc+rng, self._nbins+1),
                   np.linspace(yc-rng, yc+rng, self._nbins+1)]

        H, self._xedges, self._yedges = np.histogram2d(self.x.flatten(),
                                                       self.y.flatten(),
                                                       bins=xy_bins)
        # H needs to be rotated and flipped
        H = H.T
        # Mask pixels with a value of zero
        self._Hmasked = np.ma.masked_where(H == 0, H)

        # Plot 2D histogram using pcolor
        cmap = mpl.cm.get_cmap('viridis')
        cmap.set_bad('w')
        self._hist_im = ax.pcolormesh(self._xedges,
                                      self._yedges,
                                      self._Hmasked,
                                      cmap=cmap)

        self._circ_r_max = mpl.patches.Circle((self._xc, self._yc),
                                              self._r_max,
                                              ec='r',
                                              fc='none',
                                              ls='solid',
                                              lw=2)
        self._circ_r_min = mpl.patches.Circle((self._xc, self._yc),
                                              self._r_min,
                                              ec='r',
                                              fc='none',
                                              ls='solid',
                                              lw=1.25)

        #rwh = (self._xedges[1]-self._xedges[0])*2
        trans = ax.transData.inverted()
        rwh = (trans.transform(ax.transAxes.transform((0.02,)*2))
               - np.array(ax.axis())[0::2])
        rwh = rwh[0]
        self._rect = mpl.patches.Rectangle((self._xc-rwh/2, self._yc-rwh/2),
                                           rwh,
                                           rwh,
                                           ec='k',
                                           fc='none',
                                           lw=2)
        ax.add_patch(self._rect)
        ax.add_patch(self._circ_r_max)
        ax.add_patch(self._circ_r_min)

        if self.widget is None:
            self._hist_title = plt.title(self._hist_tit_str(), fontsize=12, y=0.98)
            plt.xlabel('x')
            plt.ylabel('y')
        else:
            self._hist_title = self.fig.suptitle(self._hist_tit_str(), fontsize=12, y=0.98)
            ax.set_xlabel('x')
            ax.set_ylabel('y')

        cbar = self.fig.colorbar(self._hist_im)
        cbar.ax.set_ylabel('Counts')

        if dark_mode:
            axcolor = 'darkgray'
            mpl.rcParams['axes.facecolor'] = "cyan"
        else:
            axcolor = 'lightgoldenrodyellow'
        # SLIDERS
        if mplv2:
            d = {'facecolor': axcolor}
        else:
            d = {'axisbg': axcolor}
        self._axgaus = self.add_axes([0.1, 0.1, 0.65, 0.03], **d)
        self._axvectrot = self.add_axes([0.1, 0.15, 0.65, 0.03], **d)
        self._sgaus = Slider(self._axgaus, 'Gaus.', 0.0, self._gaus_lim,
                             valinit=self._gaus)
        self._svectrot = Slider(self._axvectrot, 'Rot.', 0.0, 360.0,
                                valinit=self._vectrot)
        self._sgaus.on_changed(self._update_gaus)
        self._svectrot.on_changed(self._update_vectrot)

        # BUTTONS
        # save button
        axsave = self.add_axes([0.90, 0.02, 0.07, 0.05])
        self._bsave = mpl.widgets.Button(axsave, 'Save')
        self._bsave.on_clicked(self._on_save)
        # close button
        axclose = self.add_axes([0.82, 0.02, 0.07, 0.05])
        self._bclose = mpl.widgets.Button(axclose, 'Close')
        self._bclose.on_clicked(self._on_close)
        # reset dt button
        axdt = self.add_axes([0.74, 0.02, 0.07, 0.05])
        self._bdt = mpl.widgets.Button(axdt, 'R:dt')
        self._bdt.on_clicked(self._on_dt)
        # reset descan button
        axds = self.add_axes([0.66, 0.02, 0.07, 0.05])
        self._bds = mpl.widgets.Button(axds, 'R:DS')
        self._bds.on_clicked(self._on_ds)
        # reset sigma
        axsig = self.add_axes([0.58, 0.02, 0.07, 0.05])
        self._bsig = mpl.widgets.Button(axsig, 'R:sig')
        self._bsig.on_clicked(self._on_sig)
        # reset rotation
        axvec = self.add_axes([0.50, 0.02, 0.07, 0.05])
        self._bvec = mpl.widgets.Button(axvec, 'R:rot')
        self._bvec.on_clicked(self._on_vec)
        # reset r_min
        axrmin = self.add_axes([0.42, 0.02, 0.07, 0.05])
        self._brmin = mpl.widgets.Button(axrmin, 'R:rmin')
        self._brmin.on_clicked(self._on_r_min)
        # ransac button
        axran = self.add_axes([0.34, 0.02, 0.07, 0.05])
        self._bran = mpl.widgets.Button(axran, 'Ran.')
        self._bran.on_clicked(self._on_ransac)
        if self._ransac:
            if mplv2:
                self._bran.ax.set_facecolor('green')
            else:
                self._bran.ax.set_axis_bgcolor('green')

        # median button
        axmed = self.add_axes([0.26, 0.02, 0.07, 0.05])
        self._bmed = mpl.widgets.Button(axmed, 'Med.')
        self._bmed.on_clicked(self._on_median)
        if self._median:
            if mplv2:
                self._bmed.ax.set_facecolor('green')
            else:
                self._bmed.ax.set_axis_bgcolor('green')
        # print cmd
        axprint = self.add_axes([0.18, 0.02, 0.07, 0.05])
        self._bprint = mpl.widgets.Button(axprint, 'Prt')
        self._bprint.on_clicked(self._on_print)
        # write xy and print cmd
        axwxy = self.add_axes([0.10, 0.02, 0.07, 0.05])
        self._bwxy = mpl.widgets.Button(axwxy, 'xy')
        self._bwxy.on_clicked(self._on_wxy)

        # flip buttons
        axflipy = self.add_axes([0.90, 0.08, 0.07, 0.05])
        self._bflipy = mpl.widgets.Button(axflipy, 'Flip Y')
        self._bflipy.on_clicked(self._on_flipy)
        if self._flip_y:
            if mplv2:
                self._bflipy.ax.set_facecolor('green')
            else:
                self._bflipy.ax.set_axis_bgcolor('green')

        axflipx = self.add_axes([0.90, 0.14, 0.07, 0.05])

        self._bflipx = mpl.widgets.Button(axflipx, 'Flip X')
        self._bflipx.on_clicked(self._on_flipx)
        if self._flip_x:
            if mplv2:
                self._bflipx.ax.set_facecolor('green')
            else:
                self._bflipx.ax.set_axis_bgcolor('green')

        # RADIOS
        # cmaps
        active_ind = list(self._cmaps.keys()).index(self._cmap_curent[0])
        h = 0.05*len(self._cmaps)
        rax = self.add_axes([0.02, 0.9-h, 0.17, h])
        self._radio = RadioButtons(rax, self._cmaps.keys(), active=active_ind)
        self._radio.on_clicked(self._on_cmap)

        # median mode
        hm = 0.05*2+0.01
        raxm = self.add_axes([0.02, 0.9-(h+hm+0.01), 0.17, hm])
        self._radiom = RadioButtons(raxm, ['med.', 'med. of dif.'], active=self._median_mode)
        self._radiom.on_clicked(self._on_median_mode)

        # sequence
        if self._seq:
            s = '%d (+1) / %d' % (self._seq_ind, self._seq_length)
            self._seq_txt = f.text(0.095, 0.26, s, ha='center', va='bottom')

            self._axprev = self.add_axes([0.02, 0.2, 0.07, 0.05])
            self._axnext = self.add_axes([0.10, 0.2, 0.07, 0.05])
            self._bnext = mpl.widgets.Button(self._axnext, 'Next')
            self._bnext.on_clicked(self._on_seq_next)
            self._bprev = mpl.widgets.Button(self._axprev, 'Prev')
            self._bprev.on_clicked(self._on_seq_prev)

        if self.widget is None:
            plt.draw()
        else:
            docked.get_canvas().draw()

    def _on_flipy(self, event):
        self._flip_y = not self._flip_y
        self._update_calcs_and_plots()
        if self._flip_y:
            axcolor = 'green'
        else:
            axcolor = '0.85'
        if mplv2:
            self._bflipy.ax.set_facecolor(axcolor)
        else:
            self._bflipy.ax.set_axis_bgcolor(axcolor)
        self._bflipy.color = axcolor

    def _on_flipx(self, event):
        self._flip_x = not self._flip_x
        self._update_calcs_and_plots()
        if self._flip_x:
            axcolor = 'green'
        else:
            axcolor = '0.85'
        if mplv2:
            self._bflipx.ax.set_facecolor(axcolor)
        else:
            self._bflipx.ax.set_axis_bgcolor(axcolor)
        self._bflipx.color = axcolor

    def _set_seq_ind(self, i=None, update_plots=True):
        if i is not None:
            self._seq_ind = i
        self._seq_ind = self._seq_ind % self._seq_length
        self.set_yx(yx=self._seq_data[self._seq_ind], update_plots=update_plots)
        self._seq_txt.set_text('%d (+1)/ %d' % (self._seq_ind, self._seq_length))

    def _on_seq_next(self, event, update_plots=True):
        self._seq_ind += 1
        self._set_seq_ind(update_plots=update_plots)

    def _on_seq_prev(self, event, update_plots=True):
        self._seq_ind -= 1
        self._set_seq_ind(update_plots=update_plots)

    def get_image_sequence(self, im_types='tr_im', images=False):
        '''
        Get data or rendered images of a sequence or a single dataset.
        
        Parameters
        ----------
        im_types : str or list of str
            Image type(s) to return. These must be an attributes of the class.
            See the class documentation for details.
        images : bool
            If False, the raw data is returned (floats), otherwise, the
            data are returned as 8-bit images. The offset and scale are set
            appropriately for the image.  
        
        Returns
        -------
        ims : ndarray
            Image sequence(s) of shape ([im_types,], seq_len, imagey, imagex).
            The `seq_len` index is squeezed if singular.
        
        '''

        n = 1
        if self._seq:
            self._temp_seq_i = self._seq_ind
            n = self._seq_length

        if not isinstance(im_types, list):
            im_types = [im_types]

        raw = ['x', 'y', 'r']           # raw values
        zto = ['rn', 't_im', 'tr_im']   # [0, 1]
        zt2pi = ['tn']                  # [0, 2pi]

        ims = []
        for i in range(n):
            if self._seq:
                self._set_seq_ind(i, update_plots=False)
            ims_i = []
            for attr in im_types:
                im = getattr(self, attr, None)
                if attr in raw:
                    # set limits
                    if self._yx_range_from_r:
                        vmin, vmax = -self._r_max, self._r_max
                        if attr == 'r':
                            vmin, vmax = 0, self._r_max
                    else:
                        vmin, vmax = np.percentile(im, [0, 100])
                    im = im.clip(vmin, vmax)
                ims_i.append(im)
            ims.append(ims_i)
        ims = np.rollaxis(np.array(ims), 1)

        # set scaling of output
        if images:
            mins = np.zeros(len(im_types))
            maxs = np.ones(len(im_types))

            for i, imt in enumerate(im_types):
                if imt in raw:
                    # autoscale
                    mins[i], maxs[i] = np.percentile(ims[i], [0, 100], axis=(-3, -2, -1))
                elif imt in zt2pi:
                    maxs[i] = 2*np.pi
                elif imt in zto:
                    pass
                else:
                    # unknown are also autoscaled
                    print('Images of Unknown im_type %s will be autoscaled' % (imt))
                    mins[i], maxs[i] = np.percentile(ims[i], [0, 100], axis=(-3, -2, -1))

            # adjust dimensionality
            for i in range(ims.ndim-1):
                mins = mins[..., None]
                maxs = maxs[..., None]
            ims = (ims - mins) / (maxs - mins) * 255   # all [0, 255]
            ims = ims.astype('u1')
        ims = ims.squeeze()

        if self._seq:
            self._set_seq_ind(self._temp_seq_i, update_plots=True)
            del self._temp_seq_i
        return ims

    def _on_cmap(self, label):
        i = list(self._cmaps.keys()).index(label)
        self._cmap_curent = list(self._cmaps.items())[i]
        self._calc_rt()
        self._update_rt_plot()
        self._update_cw_plot_ims()

    def _on_median_mode(self, label):
        lab = self._radiom.value_selected
        labs = [t.get_text() for t in self._radiom.labels]
        index = labs.index(lab)

        self._median_mode = index
        if self._median == True:
            self._update_calcs_and_plots()

    def _update_cw_plot_ims(self):
        # function knows if figure needs updated or initialised
        self._plot_cw()

    def _update_hist_calc(self):
        # rectangle selection
        if self._xy_selector.artists[0].get_visible():
            xmin, xmax, ymin, ymax = np.round(self._xy_selector.extents).astype(int)
            x = self.x[ymin:ymax, xmin:xmax]
            y = self.y[ymin:ymax, xmin:xmax]
        else:
            x, y = self.x, self.y

        H, _, _ = np.histogram2d(x.flatten(), y.flatten(),
                                 bins=[self._xedges, self._yedges])
        # H needs to be rotated and flipped
        H = H.T
        # Mask pixels with a value of zero
        self._Hmasked = np.ma.masked_where(H == 0, H)

    def _update_hist_plot(self):
        self._update_hist_calc()
        self._hist_title.set_text(self._hist_tit_str())
        self._hist_im.set_array(self._Hmasked.flatten())
        self._hist_im.autoscale()
        self._hist_im.figure.canvas.draw_idle()

    def _plot_rt(self):
        kwd = dict(adjustable='box-forced', aspect='equal')
        if _mpl_non_adjust:
            _ = kwd.pop('adjustable')

        window_name = 'rt'
        if self.widget is not None:
            docked = self.widget.setup_docking(window_name)
            self.fig = docked.get_fig()
            self.fig.clf()

            axs = self.fig.subplots(1, 3, sharex=True, sharey=True,
                              subplot_kw=kwd)
            f = self.fig.canvas
        else:
            f, axs = plt.subplots(1, 3, sharex=True, sharey=True,
                              subplot_kw=kwd,
                              figsize=(12, 4.4))
            f.canvas.set_window_title(window_name)
            self.fig = plt
        
        ims = []
        self._figs.append(f)

        for i, (ax, d, t) in enumerate(zip(axs.flat,
                                           [self.rn]+self._t_ims,
                                           ['radius',
                                            'theta',
                                            'theta (r)'])):
            if i == 0:
                im = ax.imshow(d, interpolation='nearest', cmap='gray')
            else:
                im = ax.imshow(d, interpolation='nearest')
            ax.set_title(t)
            ax.set_axis_off()
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ims.append(im)
        plt.tight_layout()

        if self.widget is None:
            plt.draw()
        else:
            docked.get_canvas().draw()

        self._im_objs = ims

    def _plot_cw(self):
        N = 32
        t = np.radians(np.linspace(0, 360, 2*N))    # theta
        r = np.linspace(self._cw_rmin, 1, N)         # radii

        R, T = np.meshgrid(r, t)                    # meshes. T: # [0 2pi]
        values = np.random.random((t.size, r.size))
        Rn = (R-R.min())/np.ptp(R)                  # [0 1]

        A_rgb = self._cmap_curent[1](T/(2*np.pi))[..., :3]
        A_hsv = mpl.cm.colors.rgb_to_hsv(A_rgb)
        A_hsv_rv = A_hsv.copy()
        A_hsv_rv[..., 2] *= Rn
        A_rgb_rv = mpl.cm.colors.hsv_to_rgb(A_hsv_rv)

        try:
            # figure exists
            axs = self._cw_fig.axes
        except AttributeError:
            window_name = 'cw'
            # 1st run, ao make figure
            if self.widget is not None:
                docked = self.widget.setup_docking(window_name)
                self.fig = docked.get_fig()
                self.fig.clf()

                axs = self.fig.subplots(1, 2, subplot_kw=dict(projection='polar'))
                f = self.fig.canvas
            else:
                f, axs = plt.subplots(1, 2, subplot_kw=dict(projection='polar'),
                                    figsize=(6.4, 3))
                f.canvas.set_window_title(window_name)
                f.patch.set_alpha(0.0)

                self.fig = plt
            self._cw_fig = f
            self._figs.append(f)

        ims = []
        for ax, pd in zip(axs, [A_rgb, A_rgb_rv]):
            #if ax.ishold():
            #ax.hold('off')
            ax.clear()
            im = ax.pcolormesh(T, R, values, color=pd.reshape((-1, 3)),
                               shading='gouraud')
            im.set_array(None)
            ax.set_axis_off()
            ax.set_theta_offset(self._dt)
            ims.append(im)
        if self.widget is None:
            self._cw_fig.canvas.draw_idle()
        else:
            docked.get_canvas().draw_idle()

        self._cw_im_objs = ims

    def _update_cw_plot_theta(self):
        for im in self._cw_im_objs:
            im.axes.set_theta_offset(self._dt)
        im.figure.canvas.draw_idle()

    def _update_rt_plot(self):
        for imp, imd in zip(self._im_objs, [self.rn]+self._t_ims):
            imp.set_data(imd)
        self._im_objs[0].autoscale()  # for r
        imp.figure.canvas.draw_idle()

    def _on_sig(self, event):
        self._sgaus.reset()
        self._update_calcs_and_plots()

    def _on_vec(self, event):
        self._svectrot.reset()
        self._update_calcs_and_plots()

    def _on_r_min(self, event):
        self._r_min = 0
        self._circ_r_min.radius = self._r_min
        self._update_hist_plot()
        self._calc_rt()
        self._update_rt_plot()

    def save(self, working_dir=None, post_tag=None):
        '''
        Save data to timestamped directory. If part of a sequence, the
        directory is appended with `_seq%02d`, starting at 0.
        
        Parameters
        ----------
        working_dir : string or None
            Directory in which timestamped data directories are saved.
            If None, the current working directory is used.
        post_tag : string
            Appended to data directory name.
        
        Returns
        -------
        save_dir : string
            Directory of saved data.
        
        '''

        save_dir = self._on_save(None, post_tag=post_tag, working_dir=working_dir)
        return save_dir

    def _on_save(self, event, post_tag=None, working_dir=None):
        if working_dir is None:
            working_dir = os.path.abspath(os.path.curdir)
        else:
            working_dir = os.path.abspath(working_dir)
            if not os.path.exists(working_dir):
                # make dir
                print('Making directory: %s\n' % (working_dir))
                os.makedirs(working_dir)

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if post_tag is None:
            post_tag = ''
        elif post_tag.startswith('_') is False:
            post_tag = '_' + post_tag
        #path = self._create_time + '_dpc' + post_tag
        save_dir = now + '_dpc' + post_tag
        if self._seq:
            save_dir += '_seq%02d' % (self._seq_ind)
        path = os.path.join(working_dir, save_dir)
        print('saving into: ' + path)

        # self.fig windows
        if not os.path.exists(path):
            os.mkdir(path)
        for f, tag in zip(self._figs, ['xy', 'hist', 'rt', 'cw']):
            f_path = os.path.join(path, now+'_win_'+tag)
            f.savefig(f_path+'.png', bbox_inches='tight', dpi=300)

        # rt images
        for fn, imob in zip(['rn', 'tc', 'tcrv'], self._im_objs):
            im_data = imob.get_array().data
            mpl.image.imsave(os.path.join(path, now+'_'+fn+'.png'),
                             im_data, cmap='gray')

        # (y,x)
        for fn, imob in zip(['y', 'x'], self._xy_ims):
            im_data = imob.get_array().data
            np.savetxt(os.path.join(path, now+'_'+fn+'.dat.gz'), im_data)
            if self._yx_range_from_r:
                vmin, vmax = -self._r_max, self._r_max
            else:
                vmin, vmax = np.percentile(im_data, [0, 100])
            mpl.image.imsave(os.path.join(path, now+'_'+fn+'.png'),
                             im_data, cmap='gray', vmin=vmin, vmax=vmax)
        for fn, arr in zip(['y_orig', 'x_orig'], [self._y_orig, self._x_orig]):
            np.savetxt(os.path.join(path, now+'_'+fn+'.dat.gz'), arr)
            mpl.image.imsave(os.path.join(path, now+'_'+fn+'.png'),
                             arr, cmap='gray')

        # (r, theta)
        np.savetxt(os.path.join(path, now+'_'+'t'+'.dat.gz'), self._t)
        mpl.image.imsave(os.path.join(path, now+'_'+'r'+'.png'), self.r,
                         cmap='gray')
        np.savetxt(os.path.join(path, now+'_'+'r'+'.dat.gz'), self.r)
        # no color t since tc is equivalent

        # data
        dnames = ['yc', 'xc', 'r_max', 'descanY_factY', 'descanY_factX',
                  'descanX_factY', 'descanX_factX', 'dt', 'gaus',
                  'vectrot', 'r_min']
        data = ['%0.6e' % (getattr(self, '_'+t)) for t in dnames]
        data = np.column_stack((dnames+['pct', 'median', 'median_mode', 'ransac', 'ransac_dict', 'flip_y', 'flip_x', 'origin'],
                                data+[json.dumps(self._pct),
                                      json.dumps(self._median),
                                      json.dumps(self._median_mode),
                                      json.dumps(self._ransac),
                                      json.dumps(self._ransac_dict),
                                      json.dumps(self._flip_y),
                                      json.dumps(self._flip_x),
                                      json.dumps(self._origin)]))
        np.savetxt(os.path.join(path, now+'_'+'data'+'.dat'), data, fmt="%s")

        # cmd opts
        fn = os.path.join(path, now+'_'+'cmd_opts'+'.txt')
        with open(fn, "w") as text_file:
            text_file.write(self._on_print(None))

        # colorwheel
        f = self._figs[3]
        for fn, ax in zip(['flat', 'val'], f.axes):
            we = ax.get_window_extent()
            extent = we.transformed(f.dpi_scale_trans.inverted())
            f.savefig(os.path.join(path, now+'_cw_'+fn+'.png'),
                      bbox_inches=extent, dpi=300)
        print('Done')
        return path

    def _on_close(self, event):
        for f in self._figs:
            plt.close(f)
        # remove tmp files
        [os.unlink(f) for f in self._tmp_fns]

        self._disconnect()

    def _on_dt(self, event):
        self._dt = self._dt_orig
        self._update_hist_plot()
        self._calc_rt()
        self._update_rt_plot()
        self._update_cw_plot_theta()

    def _on_ds(self, event):
        self._descanY_factY = self._descanY_factX = 0
        self._descanX_factY = self._descanX_factX = 0
        self.y = self._y_orig
        self.x = self._x_orig
        self._update_calcs_and_plots()

    def _on_ransac(self, event):
        self._ransac = not self._ransac
        if self._ransac:
            axcolor = 'green'
        else:
            axcolor = '0.85'
        if mplv2:
            self._bran.ax.set_facecolor(axcolor)
        else:
            self._bran.ax.set_axis_bgcolor(axcolor)
        self._bran.color = axcolor
        self._update_calcs_and_plots(calc_ransac=self._ransac)

    def _on_median(self, event):
        self._median = not self._median
        if self._median:
            axcolor = 'green'
        else:
            axcolor = '0.85'
        if mplv2:
            self._bmed.ax.set_facecolor(axcolor)
        else:
            self._bmed.ax.set_axis_bgcolor(axcolor)
        self._bmed.color = axcolor
        self._update_calcs_and_plots()

    def _on_print(self, event):
        # print command options for current settings to stdout
        cmd_str = "r_min=%0.4f, r_max=%0.4f, descan=[%0.4f, %0.4f, %0.4f, %0.4f], cyx=[%0.4f, %0.4f], vectrot=%0.2f, gaus=%0.2f, pct=[[%0.3f, %0.3f], [%0.3f, %0.3f]], dt=%0.2f, median=%s, median_mode=%d, ransac=%s, ransac_dict=%s, flip_y=%s, flip_x=%s, origin=%s, yx_range_from_r=%s" % (
            self._r_min, self._r_max, self._descanY_factY*1000, self._descanY_factX*1000, self._descanX_factY*1000, self._descanX_factX*1000, self._yc, self._xc, self._vectrot, self._gaus, self._pct[0][0], self._pct[0][1], self._pct[1][0], self._pct[1][1], self._dt, str(self._median), self._median_mode, str(self._ransac), str(self._ransac_dict), str(self._flip_y), str(self._flip_x), self._origin, str(self._yx_range_from_r))

        print(cmd_str)
        #print('\n')
        return cmd_str

    def _on_wxy(self, event):
        # write xy data to txt file and print command
        self._on_print(None)

        np.savetxt('x.txt', self.x, fmt='%.6e')
        np.savetxt('y.txt', self.y, fmt='%.6e')
        np.savetxt('x_filt.txt', self.x, fmt='%.6e')
        np.savetxt('y_filt.txt', self.y, fmt='%.6e')

    def _connect(self):
        'connect to all the events we need'
        cnct = self._rect.figure.canvas.mpl_connect
        self._cidpress = cnct('button_press_event', self._on_press)
        self._cidrelease = cnct('button_release_event', self._on_release)
        self._cidmotion = cnct('motion_notify_event', self._on_motion)
        self._keypress = cnct('key_press_event', self._on_keypress)
        self._keyrelease = cnct('key_release_event', self._on_keyrelease)
        self._scroll = cnct('scroll_event', self._on_scroll)

    def _on_scroll(self, event):
        scrolable_axes = [self._axvectrot, self._axgaus]
        if self._seq:
            scrolable_axes += [self._axprev, self._axnext]
        if event.inaxes not in scrolable_axes:
            return

        if self._seq and event.inaxes in [self._axprev, self._axnext]:
            if event.button == 'up':
                self._on_seq_next(event)
            elif event.button == 'down':
                self._on_seq_prev(event)
            return

        if event.inaxes == self._axvectrot:
            s = self._svectrot
            delta = 0.5
        elif event.inaxes == self._axgaus:
            s = self._sgaus
            delta = 0.1

        val = s.val
        if event.button == 'up':
            new_val = val+delta
            if new_val <= s.valmax:
                s.set_val(new_val)
            else:
                s.set_val(s.valmax)
        if event.button == 'down':
            new_val = val-delta
            if new_val >= s.valmin:
                s.set_val(new_val)
            else:
                s.set_val(s.valmin)

    def _on_keypress(self, event):
        # arrow key navigation of sequence
        if self._seq:
            if event.key == "left":
                self._on_seq_prev(event)
                return
            elif event.key == "right":
                self._on_seq_next(event)
                return

        yu = False
        xu = False
        #print(event.key)
        if event.key == 'control':
            self._ctrl = True
            return
        if event.key == 'shift':
            self._shift = True
            return
        if 'ctrl+' in event.key:
            # y plane
            if 'up' in event.key:
                self._descanY_factY += self._r_max/1000
                yu = True
            if 'down' in event.key:
                self._descanY_factY -= self._r_max/1000
                yu = True
            if 'left' in event.key:
                self._descanY_factX += self._r_max/1000
                yu = True
            if 'right' in event.key:
                self._descanY_factX -= self._r_max/1000
                yu = True
        if 'alt+' in event.key:
            # x plane
            if 'up' in event.key:
                self._descanX_factY += self._r_max/1000
                xu = True
            if 'down' in event.key:
                self._descanX_factY -= self._r_max/1000
                xu = True
            if 'left' in event.key:
                self._descanX_factX += self._r_max/1000
                xu = True
            if 'right' in event.key:
                self._descanX_factX -= self._r_max/1000
                xu = True
        if yu or xu:
            # update plots
            self._update_calcs_and_plots()

    def _on_keyrelease(self, event):
        if event.key == 'control':
            self._ctrl = False
        elif event.key == 'shift':
            self._shift = False

    def _on_press(self, event):
        if event.inaxes != self._rect.axes:
            return

        contains, attrd = self._rect.contains(event)
        if contains:
            #print('event contains', self._rect.xy)
            x0, y0 = self._rect.xy   # xy is not centre (lower left?)
            self._press = x0, y0, event.xdata, event.ydata
            self._press_cnt = True
            self._yc_temp = self._yc
            self._xc_temp = self._xc
            return
        contains, attrd = self._circ_r_max.contains(event)
        if contains:
            #print('event contains', self._circ_r_max.center, event.xdata, event.ydata)
            x0, y0 = self._circ_r_max.center
            self._press = x0, y0, event.xdata, event.ydata
            self._r_max_temp = self._r_max
            self._r_min_temp = self._r_min
            self._dt_temp = self._dt

    def _on_motion(self, event):
        if self._press is None:
            return
        if event.inaxes != self._rect.axes:
            return
        x0, y0, xpress, ypress = self._press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        if self._press_cnt:
            #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %(x0, xpress, event.xdata, dx, x0+dx))
            self._rect.set_x(x0+dx)
            self._rect.set_y(y0+dy)
            self._yc = self._yc_temp+dy
            self._xc = self._xc_temp+dx
            self._circ_r_max.center = (self._xc, self._yc)
            self._circ_r_min.center = (self._xc, self._yc)
            #print(dy, dx)
        else:
            # must be in circle
            #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f'%(x0, xpress, event.xdata, dx, x0+dx))
            r0 = ((xpress-x0)**2+(ypress-y0)**2)**0.5
            t0 = np.arctan2(ypress-y0, xpress-x0)
            r = ((event.xdata-x0)**2+(event.ydata-y0)**2)**0.5
            t = np.arctan2(event.ydata-y0, event.xdata-x0)
            dt = -(t-t0)
            if self._ctrl:
                #print(dt)
                self._dt = self._dt_temp+dt
            elif self._shift:
                # change r_min
                self._r_min = self._r_min_temp + r-r0
                self._circ_r_min.set_radius(self._r_min)
            else:
                #print(xpress, event.xdata, x0, r, r0, r/r0, self._r_max)
                self._r_max = self._r_max_temp + r-r0
                self._circ_r_max.set_radius(self._r_max)
        self._hist_title.set_text(self._hist_tit_str())
        self._rect.figure.canvas.draw_idle()

        '''
        # faster drawing, but processing time leads to que and draw doesn't
        # clear till after release
        # http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
        self._rect.axes.draw_artist(self._rect)
        self._rect.axes.draw_artist(self._circ_r_max)
        self._rect.figure.canvas.update()
        self._rect.figure.canvas.flush_events()
        '''

        self._calc_rt()
        self._update_rt_plot()

    def _on_release(self, event):
        # reset the press data
        self._press = None
        self._press_cnt = False
        self._yc_temp = None
        self._xc_temp = None
        self._r_max_temp = None
        self._r_min_temp = None
        self._dt_temp = None
        self._rect.figure.canvas.draw_idle()
        self._update_cw_plot_theta()
        self._update_xy_plot()   # update x, y plots after dragging stopped

    def _disconnect(self):
        # disconnect all the stored connection ids
        self._rect.figure.canvas.mpl_disconnect(self._cidpress)
        self._rect.figure.canvas.mpl_disconnect(self._cidrelease)
        self._rect.figure.canvas.mpl_disconnect(self._cidmotion)
        self._rect.figure.canvas.mpl_disconnect(self._keypress)
        self._rect.figure.canvas.mpl_disconnect(self._keyrelease)
        self._rect.figure.canvas.mpl_disconnect(self._scroll)

    def plot_cmap_ordinates(self, n=8, endpoint=True):
        '''
        Plot ordinates of colourmaps in seperate figures.
        
        Parameters
        ----------
        n : int
            Number of angles (excluding 360 degrees).
        endpoint : bool
            If True, add 360 (==0) degrees to plot.
        
        '''

        import matplotlib.patches as patches
        if endpoint:
            n += 1
        for cmap in self._cmaps.values():
            clrs = cmap(np.linspace(0, 360, n, endpoint=endpoint)/360.0)
            clrs[-1] = clrs[0]
            plt.figure()
            ax = plt.gca()
            for i, c in enumerate(clrs):
                rect = patches.Rectangle((i, 0), 1, 3, linewidth=0, edgecolor=None, facecolor=c)
                ax.add_patch(rect)
            plt.axis([0, len(clrs), 0, 3])

    def set_yx(self, y=None, x=None, yx=None, update_plots=True):
        '''
        Set one or both of y and x data and, optionally, update plots.
        The data arrays are always updated.
        
        Parameters
        ----------
        y : 2-D array or None
            New y data.
        x : 2-D array or None
            New x data.
        yx : array-like or None
            New yx data (in 1st dimension).
        update_plots : bool
            If True, update plots.
        
        Notes
        -----
        The new data need not be of the same shape as the previous data,
        however, the edges used for the histogram are not currently updated.
               
        '''

        if y is not None:
            self._y_orig = y
        if x is not None:
            self._x_orig = x
        if yx is not None:
            self._y_orig, self._x_orig = yx

        if not ((y is None) & (x is None) & (yx is None)):
            self._make_scan_indices()
            if update_plots:
                self._update_calcs_and_plots(calc_ransac=self._ransac)
            else:
                self._calc_data(calc_ransac=self._ransac)
                self._calc_rt()
                self._update_hist_calc()
        else:
            print('Nothing to update.')

    def add_axes(self,*argv, **kwargs):
        if self.widget is None:
            return plt.axes(*argv,**kwargs)
        else:
            return self.fig.add_axes(*argv, **kwargs)
