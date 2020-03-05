import fpd
from fpd import fpd_processing as fpdp
from fpd import _p3
import sys
import multiprocessing as mp
import tqdm
import numpy as np
from . import fpd_processing as fpdp_new

import numpy as np
import scipy as sp
from scipy.ndimage.filters import gaussian_filter, gaussian_filter1d
#from scipy.ndimage.measurements import center_of_mass
from scipy.signal import fftconvolve

import matplotlib as mpl
import matplotlib.pyplot as plt

from skimage.feature import canny, peak_local_max
from skimage.transform import hough_circle
from skimage import color
from skimage.draw import circle_perimeter
from skimage.feature import register_translation
#from skimage.transform import pyramid_expand
from skimage.filters import threshold_otsu
from skimage.morphology import disk, binary_closing, binary_opening

import h5py
import datetime
import os
import multiprocessing as mp
from functools import partial
import sys
import itertools
import collections
import time
import warnings
from numbers import Number
from tqdm import tqdm

from itertools import combinations
from collections import namedtuple

from fpd.fpd_processing import _p3

def phase_correlation(data, nr, nc, cyx=None, crop_r=None, sigma=2.0,
                      spf=100, pre_func=None, post_func=None, mode='2d',
                      ref_im=None, rebin=None, der_clip_fraction=0.0,
                      der_clip_max_pct=99.9, truncate=4.0, parallel=True,
                      ncores=None, print_stats=True, nrnc_are_chunks=False, origin='top', 
                      logger=None):
    '''
    Perform phase correlation on 4-D data using efficient upscaling to
    achieve sub-pixel resolution.
    
    Parameters
    ----------
    data : array_like
        Mutidimensional data of shape (scanY, scanX, ..., detY, detX).
    nr : integer or None
        Number of rows to process at once.
    nc : integer or None
        Number of columns to process at once.
    cyx : length 2 iterable or None
        Centre of disk in pixels (cy, cx).
        If None, centre is used.
    crop_r : scalar or None
        Radius of circle about cyx defining square crop limits used for
        cross-corrolation, in pixels.
        If None, the maximum square array about cyx is used.
    sigma : scalar
        Smoothing of Gaussian derivitive.
    spf : integer
        Sub-pixel factor i.e. 1/spf is resolution.
    pre_func : callable
        Function that operates (out-of-place) on data before processing.
        out = pre_func(in), where in is nd_array of shape (n, detY, detX).
    post_func : callable
        Function that operates (out-of-place) on data after derivitive.
        out = post_func(in), where in is nd_array of shape (n, detY, detX).
    mode : string
        Derivative type. 
        If '1d', 1d convolution; faster but not so good for high sigma.
        If '2d', 2d convolution; more accurate but slower.
    ref_im : None or ndarray
        2-D image used as reference. 
        If None, the first probe position is used.
    rebin : integer or None
        Rebinning factor for detector dimensions. None or 1 for none. 
        If the value is incompatible with the cropped array shape, the
        nearest compatible value will be used instead. 
        'cyx' and 'crop_r' are for the original image and need not be modified.
        'sigma' and 'spf' are scaled with rebinning factor, as are output shifts.
    der_clip_fraction : float
        Fraction of `der_clip_max_pct` in derivative images below which will be
        to zero.
    der_clip_max_pct : float
        Percentile of derivative image to serve as reference for `der_clip_fraction`.
    truncate : scalar
        Number of sigma to which Gaussians are calculated.
    parallel : bool
        If True, derivative and correlation calculations are multiprocessed.
        Note, if `mode=1d`, the derivative calculations are not multiprocessed,
        but may be multithreaded if enabled in the numpy linked BLAS lib.
    ncores : None or int
        Number of cores to use for mutliprocessing. If None, all cores
        are used.
    print_stats : bool
        If True, statistics on the analysis are printed.
    nrnc_are_chunks : bool
        If True, `nr` and `nc` are interpreted as the number of chunks to
        process at once. If `data` is not chunked, `nr` and `nc` are used
        directly.
    origin : str
        Controls y-origin of returned data. If origin='top', pythonic indexing 
        is used. If origin='bottom', increasing y is up.
        
    Returns
    -------
    Tuple of (shift_yx, shift_err, shift_difp, ref), where:
    shift_yx : array_like
        Shift array in pixels, of shape ((y,x), scanY, scanX, ...).
        Increasing Y, X is disc shift up, right in image.
    shift_err : 2-D array
        Translation invariant normalized RMS error in correlations.
        See skimage.feature.register_translation for details.
    shift_difp : 2-D array
        Global phase difference between the two images.
        (should be zero if images are non-negative).
        See skimage.feature.register_translation for details.
    ref : 2-D array
        Reference image.
    
    Notes
    -----
    The order of operations is rebinning, pre_func, derivative, 
    post_func, and correlation.
    
    If `nr` or `nc` are None, the entire dimension is processed at once.
    For chunked data, setting `nrnc_are_chunks` to True, and `nr` and `nc`
    to a suitable values can improve performance.
    
    Specifying 'crop_r' (and appropriate cyx) can speed up calculation significantly.
    
    The execution of 'pre_func' and 'post_func' are not multiprocessed, so 
    they could employ multiprocessing for cpu intensive calculations.
    
    Efficient upscaling is based on:
    http://scikit-image.org/docs/stable/auto_examples/transform/plot_register_translation.html
    http://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.register_translation
    
    '''
    
    # der_clip_max_pct=99.9 'ignores' (256**2)*0.001 ~ 65 pixels.
    # (256**2)*0.001 / (2*3.14) / 2 ~ 5. == ignoring of 5 pix radius, 2 pix width torus
    
    if nrnc_are_chunks:
        nr, nc = fpdp._condition_nrnc_if_chunked(data, nr, nc, print_stats)
    
    if ncores is None:
        ncores = mp.cpu_count()
    
    nondet = data.shape[:-2]
    nonscan = data.shape[2:]
    scanY, scanX = data.shape[:2]
    detY, detX = data.shape[-2:]
    
    r_if, c_if = fpdp._block_indices((scanY, scanX), (nr, nc))
    
    rtn = fpdp._parse_crop_rebin(crop_r, detY, detX, cyx, rebin, print_stats)
    cropped_im_shape, rebinf, rebinning, rii, rif, cii, cif = rtn
       
    
    # rebinning
    rebinf = 1
    rebinning = rebin is not None and rebin != 1
    if rebinning:
        f, fs = fpdp._find_nearest_int_factor(cropped_im_shape[0], rebin)
        if rebin != f:
            print('Image data cropped to:', cropped_im_shape)
            print('Requested rebin (%d) changed to nearest value: %d. Possible values are:' %(rebin, f), fs)
            rebin = f
        rebinf = rebin
        sigma = float(sigma)/rebinf
        spf = int(float(spf)*rebinf)
    rebinned_im_shape = tuple([x//rebinf for x in cropped_im_shape])
    #print('Cropped shape: ', cropped_im_shape)
    #if rebinning:
        #print('Rebinned cropped shape: ', rebinned_im_shape)
    
    
    # gradient of gaussian
    gy, gx = fpdp._g2d_der(sigma, truncate=truncate)
    gxy = gx + 1j*gy
    #gxy = (gx**2 + gy**2)**0.5
    
    
    ### ref im
    if ref_im is None:
        # use first point
        ref_im = data[0, 0, ...]
        for i in range(len(nondet)-2):
            ref_im = ref_im[0]
    else:
        # provided option
        ref_im = ref_im
    
    ref = ref_im[rii:rif+1, cii:cif+1]
    for t in range(len(nondet)): 
        ref = np.expand_dims(ref, 0)    # ref[None, None, None, ...]
    if rebinning:
        ns = ref.shape[:-2] + tuple([int(x/rebin) for x in ref.shape[-2:]])
        ref = fpdp.rebinA(ref, *ns)
    ref = fpdp._process_grad(ref, pre_func, mode, sigma, truncate, gxy,
                        parallel, ncores, der_clip_fraction, der_clip_max_pct,
                        post_func)[0]
    
    
    shift_yx = np.empty(nondet + (2,))
    shift_err = np.empty(nondet)
    shift_difp = np.empty_like(shift_err)
    
    if print_stats:
        print('\nPerforming phase correlation')
        tqdm_file = sys.stderr
    else:
        tqdm_file = fpdp.DummyFile()
    total_nims = np.prod(nondet)
    with tqdm(total=total_nims, file=tqdm_file, mininterval=0, leave=True, unit='images') as pbar:
        for i, (ri, rf) in enumerate(r_if):
            for j, (ci, cf) in enumerate(c_if):               
                # read selected data (into memory if hdf5)  
                d = data[ri:rf, ci:cf, ..., rii:rif+1, cii:cif+1]
                d = np.ascontiguousarray(d)
                if rebinning:
                    ns = d.shape[:-2] + tuple([int(x/rebinf) for x in d.shape[-2:]])
                    d = fpdp.rebinA(d, *ns)
                
                # calc grad
                gm = fpdp._process_grad(d, pre_func, mode, sigma, truncate, gxy,
                                   parallel, ncores, der_clip_fraction, der_clip_max_pct,
                                   post_func)
                
                # Could combine grad and reg to skip ifft/fft,
                # and calc ref grad fft only once
                # For 1d mode, could try similar combinations, but using 
                # functions across ndarray axes with multithreaded blas.
                
                ## do correlation
                # gm is (n, detY, detX), with last 2 rebinned
                partial_reg = fpdp.partial(fpdp.register_translation, ref, upsample_factor=spf)
                
                if parallel:
                    pool = mp.dummy.Pool(ncores)
                    rslt = pool.map(partial_reg, gm)
                    pool.close()
                else:
                    rslt = list(map(partial_reg, gm))
                shift, error, phasediff = np.asarray(rslt).T
                shift = np.array(shift.tolist())
                # -ve shift to swap source/ref coords to be consistent with 
                # other phase analyses
                shift *= -1.0
                
                shift_yx[ri:rf, ci:cf].flat = shift
                shift_err[ri:rf, ci:cf].flat = error
                shift_difp[ri:rf, ci:cf].flat = phasediff
                
                pbar.update(np.prod(d.shape[:-2]))
    if print_stats:
        print('')
        sys.stdout.flush()    
    shift_yx = np.rollaxis(shift_yx, -1, 0)
       
    # reverse y for shift up being positive
    flp = np.array([-1, 1])
    for i in range(len(nonscan)):
        flp = np.expand_dims(flp, -1)
    shift_yx = shift_yx*flp
    
    # default origin implementation is bottom
    if origin.lower() == 'top':
        shift_yx[0] = -shift_yx[0]
        
    # scale shifts for rebinning
    if rebinning:
        shift_yx *= rebinf
    
    # print stats
    if print_stats:
        if logger is not None:
            logger.log(fpdp_new.print_shift_stats(shift_yx, to_str=True))
        else:
            fpdp_new.print_shift_stats(shift_yx)

    return shift_yx, shift_err, shift_difp, ref


def find_matching_images(images, aperture=None, avg_nims=3, cut_len=20, plot=True, widget=None):
    '''
    Finds matching images using euclidean normalised mean square error through
    all combinations of a given number of images.
    
    Parameters
    ----------
    images : ndarray
        Array of images with image axes in last 2 dimensions.
    aperture : 2D array
        An aperture to apply to the images.
    avg_nims : int
        The number of images in a combination.
    cut_len : int
        The number of combinations in which to look for common images.
    
    Returns
    -------
    named tuple 'matching' containing:
    
    yxi_combos : tuple of two 2-D arrays
        y- and x-indices of combinations, sorted by match quality.
    yxi_common :
        y- and x-indices of most common image in ``cut_len`` combinations.
    ims_common : 3-D array
        All images in in ``cut_len`` combinations matched with most common image.
    ims_best : 3-D array
        Best matching ``avg_nims`` images.
    
    Notes
    -----
    The number of combinations increases very rapidly with ``avg_nims`` and
    the number of images. Using around 100 or so images runs relatively quickly.
    
    Examples
    --------
    >>> from fpd.synthetic_data import disk_image, shift_array, shift_images
    >>> import fpd.fpd_processing as fpdp

    Generate synthetic data.
    >>> disc = disk_image(radius=32, intensity=64)
    >>> shift_array = shift_array(6, shift_min=-1, shift_max=1)

    Set shifts on diagonal to zero.
    >>> diag_inds = [np.diag(x) for x in np.indices(shift_array[0].shape)]
    >>> shift_array[0][diag_inds] = 0
    >>> shift_array[1][diag_inds] = 0
    
    Generate shifted images.
    >>> images = shift_images(shift_array, disc, noise=False)
    >>> aperture = fpdp.synthetic_aperture(images.shape[-2:], cyx=(128,)*2, rio=(0, 48), sigma=0, aaf=1)[0]
    
    Find matching images.
    >>> matching = fpdp.find_matching_images(images, aperture, plot=True)
    >>> ims_best = matching.ims_best.mean(0)
    
    '''

    # convert dask and other out-of-core to numpy
    ims_orig = np.ascontiguousarray(images)

    # flatten original images
    ims_orig_shape = ims_orig.shape
    ims_orig.shape = (-1,) + ims_orig.shape[-2:]
    n_ims = ims_orig.shape[0]

    # apply aperture and crop
    if aperture is not None:
        ri, rf = np.where(aperture.sum(0))[0][[0, -1]]
        ci, cf = np.where(aperture.sum(1))[0][[0, -1]]
        sr = slice(ri, rf + 1)
        sc = slice(ci, cf + 1)
        aperture = aperture[sr, sc]
        ims = ims_orig[:, sr, sc] * (aperture[None, ...].astype(int))
    else:
        ims = ims_orig

    # calculate nrsme for all combinations in one half diagonal
    err = np.ones((n_ims, n_ims), dtype=float)
    err[:] = np.nan
    print('Calculating NRSME for all image combinations')
    for ri, ref_im in enumerate(tqdm(ims)):
        test_ims = ims[:ri]
        err_col = fpdp.nrmse(ref_im, test_ims)
        err[:ri, ri] = err_col
    if plot:
        windowname = 'Unique images in 1st %d combinations of %d images\nsharing most common image' % (
            cut_len, avg_nims)
        if widget is not None:
            docked = widget.setup_docking("NRSME", "Top", figsize=(8, 4))
            fig = docked.get_fig()
            fig.clf()
            (ax1, ax2) = fig.subplots(1, 2, sharex=False, sharey=False)
            f = fig.canvas

        else:
            f, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(8, 4))
        ax1.imshow(err, interpolation="nearest")
        ax1.set_xlabel('Flattened image index')
        ax1.set_ylabel('Flattened image index')
        ax1.set_title("NRSME")

        '''
        import hyperspy.api as hs
        err_ims = np.reshape(err, (-1,) + ims_orig_shape[:2])
        hs.signals.Signal2D(err_ims).plot()
        '''
    # loop over all combinations
    print('Calculating combined NRSME for all combinations of %d images' % (avg_nims))
    combs_tot = int(np.math.factorial(n_ims) / (np.math.factorial(avg_nims) * np.math.factorial(n_ims - avg_nims)))
    comb_vals = np.empty(combs_tot, dtype=float)
    comb_inds = np.empty((combs_tot, avg_nims), dtype=int)
    for i, inds in enumerate(tqdm(combinations(range(n_ims), avg_nims), total=combs_tot)):
        # calculate rmse from values at intercepts of row and column slices
        ind_perms = np.array(list(combinations(inds, 2))).T
        intercept_vals = err[ind_perms[0], ind_perms[1]]
        comb_vals[i] = np.nansum(intercept_vals**2).sum()**0.5
        comb_inds[i] = inds

    # sort perms by rmse
    si = np.argsort(comb_vals)
    comb_vals = comb_vals[si]
    comb_inds = comb_inds[si]

    if plot:
        # Combined NRSME
        ax2.semilogx(comb_vals)
        ax2.set_xlabel('Combination index')
        ax2.set_ylabel('Combined NRSME')
        ax2.set_title('%d combinations of %d images' % (combs_tot, avg_nims))
        if widget is None:
            plt.tight_layout()

        # map of scan locations
        gri, gci = np.unravel_index(comb_inds, ims_orig_shape[:2])
        map_im = np.zeros(ims_orig_shape[:2])
        for i in range(cut_len):
            map_im[gri[i], gci[i]] += 1

        if widget is not None:
            docked = widget.setup_docking("", "Top", figsize=(8, 4))
            fig = docked.get_fig()
            fig.clf()
            (ax1, ax2) = fig.subplots(1, 2, sharex=False, sharey=False)
            f = fig.canvas

        else:
            f, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(8, 4))
        ax1.imshow(map_im)
        ax1.set_xlabel('Scan X index')
        ax1.set_ylabel('Scan Y index')
        ax1.set_title('First % d combinations of % d images' % (cut_len, avg_nims))

    # find most common scan index within cut
    common_im_ind = np.bincount(comb_inds[:cut_len].flat).argmax()
    print('Most common scan index in 1st %d combinations of %d images:' %
          (cut_len, avg_nims), np.unravel_index(common_im_ind, ims_orig_shape[:2]))
    contains_common_im = (comb_inds[:cut_len] == common_im_ind).sum(1) > 0

    # unique image indices within cut with most popular image in common
    common_im_inds = np.unique(comb_inds[:cut_len][contains_common_im].flatten())
    print('Number of unique images in these combinations sharing this index: %d' % (len(common_im_inds)))
    if plot:
        # plot unique points
        sel_im = np.zeros(ims_orig_shape[:2])
        sel_im.flat[common_im_inds] = 1
        ax2.imshow(sel_im)
        ax2.set_xlabel('Scan X index')
        #plt.ylabel('Scan Y index')
        if widget is None:
            plt.title(windowname)

    # calculate means and stds with mask if specified
    if plot:
        if widget is not None:
            docked = widget.setup_docking("", "Top", figsize=(5,8))
            fig = docked.get_fig()
            fig.clf()
            axs = fig.subplots(3, 2, sharex=True, sharey=True)
            f = fig.canvas
        else:
            f, axs = plt.subplots(3, 2, sharex=True, sharey=True, figsize=(5, 8))
        ax1, ax2, ax3, ax4, ax5, ax6 = axs.flatten()

        im_common = ims[common_im_inds]
        im_common_mean = im_common.mean(0)
        im_common_std = im_common.std(0)
        ax1.imshow(im_common_mean)
        ax2.imshow(im_common_std)
        ax1.set_title('Most common %d best' % (len(common_im_inds)))

        im_best = ims[comb_inds[0]]
        im_best_mean = im_best.mean(0)
        im_best_std = im_best.std(0)
        ax3.imshow(im_best_mean)
        ax4.imshow(im_best_std)
        ax3.set_title('Best combination of %d' % (avg_nims))

        im_worst = ims[comb_inds[-1]]
        im_worst_mean = im_worst.mean(0)
        im_worst_std = im_worst.std(0)
        ax5.imshow(im_worst_mean)
        ax6.imshow(im_worst_std)
        ax5.set_title('Worst combination of %d' % (avg_nims))
    print('')

    # return data (without masks)
    yxi_combos = np.unravel_index(comb_inds, ims_orig_shape[:2])
    yxi_common = np.unravel_index(common_im_inds, ims_orig_shape[:2])

    ims_common = ims_orig[common_im_inds]
    ims_common_mean = ims_common.mean(0)
    ims_common_std = ims_common.std(0)

    ims_best = ims_orig[comb_inds[0]]
    ims_best_mean = ims_best.mean(0)
    ims_best_std = ims_best.std(0)

    # reshape original, in case ascontiguousarray returns view
    ims_orig.shape = ims_orig_shape

    rtn = namedtuple('matching', ['yxi_combos', 'yxi_common', 'ims_common', 'ims_best'])
    return rtn(yxi_combos, yxi_common, ims_common, ims_best)

def disc_edge_sigma(im, sigma=2, cyx=None, r=None, use_hyperspy=False, plot=True, widget=None, logger=None):
    '''
    Calculates disc edge width by averaging sigmas from fitting Erfs to unwrapped disc.
    
    Parameters
    ----------
    im : 2-D array
        Image of disc.
    sigma : scalar
        Estimate of edge stdev.
    cyx : length 2 iterable or None
        Centre coordinates of disc. If None, these are calculated.
    r : scalar or None
        Disc radius in pixels. If None, the value is calculated.
    use_hyperspy : bool
        If True, HyperSpy is used for fitting and plotting. If False,
        scipy and matplotlib are used.
    plot : bool
        Determines if images are plotted.
    
    Returns
    -------
    sigma_wt_avg : scalar
        Average sigma value, weighted if possible by fit error.
    sigma_wt_std : scalar
        Average sigma standard deviation, weighted if possible by fit error.
        Nan if no weighting is posible.
    sigma_std : scalar
        Standard deviation of all sigma values.
    (sigma_vals, sigma_stds) : tuple of 1-D arrays
        Sigma values and standard deviations from fit.
    
    Notes
    -----
    `sigma` is used for initial value and for setting range of fit.
    Increasing value widens region fitted to.
    
    Examples
    --------
    >>> import fpd
    >>> import matplotlib.pylab as plt
    >>>
    >>> plt.ion()
    >>>
    >>> im = fpd.synthetic_data.disk_image(intensity=16, radius=32, sigma=5.0, size=256, noise=True)
    >>> cyx, r = fpd.fpd_processing.find_circ_centre(im, 2, (22, int(256/2.0), 1), spf=1, plot=False)
    >>>
    >>> returns = fpd.fpd_processing.disc_edge_sigma(im, sigma=6, cyx=cyx, r=r, plot=True)
    >>> sigma_wt_avg, sigma_wt_std, sigma_std, (sigma_vals, sigma_stds) = returns

    '''
    

    detY, detX = im.shape
    
    if cyx is None or r is None:
        cyx_, r_ = fpdp_new.find_circ_centre(im, 2, (3, int(detY / 2.0), 1), spf=1, plot=plot, widget=widget)
    if cyx is None:
        cyx = cyx_
    if r is None:
        r = r_
    cy, cx = cyx
    
    # set up coordinated
    yi, xi = np.indices((detY, detX), dtype=float)
    yi-=cy
    xi-=cx
    ri2d = (yi**2+xi**2)**0.5
    ti2d = np.arctan2(yi, xi)

    interp_pix = 0.25   # interpolation resolution
    rr, tt = np.meshgrid(np.arange(0, 2.5*r, interp_pix), 
                         np.arange(-180,180,1*4)/180.0*np.pi, 
                         indexing='ij')
    xx = rr*np.sin(tt)+cx
    yy = rr*np.cos(tt)+cy

    # MAP TO RT  
    rt_val = sp.ndimage.interpolation.map_coordinates(im.astype(float), 
                                                      np.vstack([yy.flatten(), xx.flatten()]) )
    rt_val = rt_val.reshape(rr.shape)

    if plot:
        if widget is not None:
            fig = widget.setup_docking("Aperture")
            ax = fig.get_fig().subplots()
            ax.matshow(rt_val)
            docked = widget.setup_docking("", "Top", figsize=(6, 8))
            fig = docked.get_fig()
            fig.clf()
            ax = fig.subplots(1, 1)
            f = fig.canvas

            ax.plot(rt_val[:,::18])
            ax.set_xlabel('Interp pixels')
            ax.set_ylabel('Intensity')

        else:
            plt.matshow(rt_val)
            plt.figure()
            plt.plot(rt_val[:,::18])
            plt.xlabel('Interp pixels')
            plt.ylabel('Intensity')
    
    
    # Fit edge
    der = -np.diff(rt_val, axis=0)
    
    # fit range
    ri2d_edge_min = np.concatenate((ri2d[[0, -1], :], ri2d[:, [0, -1]].T), axis=1).min()
    rmin = max( (r-3*sigma), 0 )
    rmax = min( (r+3*sigma), ri2d_edge_min )
    
    if use_hyperspy:
        from hyperspy.signals import EELSSpectrum
        from hyperspy.component import Component
        s = EELSSpectrum(rt_val.T)
        #s.align1D()
        #s.plot()
        
        s_av = s#.sum(0)
        #s_av.plot()
    
        s_av.metadata.set_item("Acquisition_instrument.TEM.Detector.EELS.collection_angle", 1)
        s_av.metadata.set_item("Acquisition_instrument.TEM.beam_energy ", 1)
        s_av.metadata.set_item("Acquisition_instrument.TEM.convergence_angle", 1)
    
        m = s_av.create_model(auto_background=False)
    
        # http://hyperspy.org/hyperspy-doc/v0.8/user_guide/model.html   
        class My_Component(Component):
            """
            """
            def __init__(self, origin=0, A=1, sigma=1):
                # Define the parameters
                Component.__init__(self, ('origin', 'A', 'sigma'))
                #self.name = 'Erf'

                # Optionally we can set the initial values
                self.origin.value = origin
                self.A.value = A
                self.sigma.value = sigma

            # Define the function as a function of the already defined parameters, x
            # being the independent variable value
            def function(self, x):
                p1 = self.origin.value
                p2 = self.A.value
                p3 = self.sigma.value
                #return p1 + x * p2 + p3
                return p2*( sp.special.erf( (x-p1)/(np.sqrt(2)*p3) )+1.0 ) /2.0

        g = My_Component()
        m.append(g)
        
        # set defaults
        sigma = sigma
        m.set_parameters_value('sigma',  sigma/interp_pix, component_list=[g])
        m.set_parameters_value('A', -np.percentile(rt_val, 90), component_list=[g])
        m.set_parameters_value('origin', r/interp_pix, component_list=[g])
        
        # set fit range
        m.set_signal_range(rmin/interp_pix, rmax/interp_pix)
        
        m.multifit()
        if plot:
            m.plot()

        sigma_vals = np.abs(g.sigma.map['values'])*interp_pix
        sigma_stds = np.abs(g.sigma.map['std'])*interp_pix
    else:
        # non-hyperspy
        from scipy.optimize import curve_fit
        
        def function(x, p1, p2, p3):
            #p1, p2, p3 = origin, A, sigma
            return p2*( sp.special.erf( (x-p1)/(np.sqrt(2)*p3) )+1.0 ) /2.0
        
        # fit range
        x = np.arange(len(rt_val))
        xmin, xmax = rmin/interp_pix, rmax/interp_pix
        b = np.logical_and(x >= xmin, x <= xmax) 
        
        p0 = (r/interp_pix, -np.percentile(rt_val, 90), sigma/interp_pix)
        popts = []
        perrs = []
        for rt_vali in rt_val.T:
            yi = rt_vali[b]
            xi = x[b]
            popt, pcov = curve_fit(f=function, xdata=xi, ydata=yi, p0=p0)
            perr = np.sqrt(np.diag(pcov))
            
            popts.append(popt)
            perrs.append(perr)
        popts = np.array(popts)
        perrs = np.array(perrs)
        
        sigma_vals = np.abs(popts[:, 2])*interp_pix
        sigma_stds = np.abs(perrs[:, 2])*interp_pix
        
        if plot:
            A = np.percentile(popts[:, 1], 50)
            fits = np.array([function(x, *pi) for pi in popts])
            
            inds = np.arange(len(sigma_vals))[::10]
            if widget is not None:
                docked = widget.setup_docking("", "Top", figsize=(6,8))
                fig = docked.get_fig()
                fig.clf()
                ax = fig.subplots(1, 1)
                f = fig.canvas
            else:
                f, ax = plt.subplots(1, 1, figsize=(6, 8))
            pad = 0.2 * A
            for j,i in enumerate(inds):
                ax.plot(x, rt_val[:, i] + pad*j, 'x')
                ax.plot(x[b], fits[i][b] + pad*j, 'b-')
            pass
    
    # calculate averages
    sigma_std = sigma_vals.std()
    
    err_is = np.where(np.isfinite(sigma_stds))[0]
    if err_is.size > 1:
        if logger is not None:
            logger.log('Calculating weighted average...')
        else:
            print('Calculating weighted average...')
        vs = sigma_vals[err_is]
        ws = 1.0/sigma_stds[err_is]**2
        sigma_wt_avg = (vs*ws).sum()/ws.sum()
        sigma_wt_std = (1.0/ws.sum())**0.5
    else:
        if logger is not None:
            logger.log('Calculating unweighted average...')
        else:
            print('Calculating unweighted average...')

        sigma_wt_avg = sigma_vals.mean()
        sigma_wt_std = np.nan
    
    
    
    sigma_pcts = np.percentile(sigma_vals, [10, 50, 90])
    if logger is not None:
        logger.log('Avg: %0.3f +/- %0.3f' % (sigma_wt_avg, sigma_wt_std))
        logger.log('Std: %0.3f' % (sigma_std))
        logger.log('Percentiles (10, 50, 90): %0.3f, %0.3f, %0.3f' % tuple(sigma_pcts))
    else:
        print('Avg: %0.3f +/- %0.3f' % (sigma_wt_avg, sigma_wt_std))
        print('Std: %0.3f' % (sigma_std))
        print('Percentiles (10, 50, 90): %0.3f, %0.3f, %0.3f' %tuple(sigma_pcts))
    
    return(sigma_wt_avg, sigma_wt_std, sigma_std, (sigma_vals, sigma_stds))

def make_ref_im(image, edge_sigma, aperture=None, upscale=4, bin_opening=None, bin_closing=None, 
    crop_pad=False, threshold=None, plot=True, widget=None):
    '''
    Generate a cleaned version of the image supplied for use as a reference.
    
    Parameters
    ----------
    image : 2-D array
        Image to process.
    edge_sigma : float
        Edge width in pixels.
    aperture : None or 2-D array
        If not None, the data will be multiplied by the aperture mask.
    upscale : int
        Upscaling factor.
    bin_opening : None or int
        Circular element radius used for binary opening.
    bin_closing : None or int
        Circular element radius used for binary closing.
    crop_pad : bool
        If True and ``aperture`` is not None, the image is cropped before
        upscaling and padded in returned image for efficiency.
    threshold : scalar or None
        Image threshold. If None, Otsu's method is used. Otherwise, the scalar
        value is used.
    plot : bool
        If True, the images are plotted.
    
    Notes
    -----
    The sequence of operation is:
        apply aperture
        upscale
        threshold
        bin_opening
        bin_closing
        edge_sigma
        downscale
        scale magnitude
    
    Examples
    --------
    >>> from fpd.synthetic_data import disk_image
    >>> import fpd.fpd_processing as fpdp

    Generate synthetic image
    >>> image = disk_image(radius=32, intensity=64)
    
    Get centre and edge, and make aperture
    >>> cyx, cr = fpdp.find_circ_centre(image, sigma=6, rmms=(2, int(image.shape[0]/2.0), 1), plot=False)
    >>> edge_sigma = fpdp.disc_edge_sigma(image, sigma=2, cyx=cyx, r=cr, plot=False)[0]
    >>> aperture = fpdp.synthetic_aperture(image.shape[-2:], cyx=cyx, rio=(0, cr+16), sigma=0, aaf=1)[0]
    
    Make reference image
    >>> ref_im = fpdp.make_ref_im(image, edge_sigma, aperture)
    
    '''
    
    # float
    im = image.astype(float)
    im_shape = image.shape
    
    # mask
    if aperture is not None:
        im = im*aperture
        if crop_pad:
            #crop and pad for efficiency
            ci, cf = np.where((aperture>0.5).sum(0)>0)[0][[0, -1]]
            ri, rf = np.where((aperture>0.5).sum(0)>0)[0][[0, -1]]
            im = im[ri:rf+1, ci:cf+1]
        
    
    # upscale and threshold
    ref_imu = sp.ndimage.interpolation.zoom(im, zoom=4, output=None,
                                            order=3, mode='constant',
                                            cval=0.0, prefilter=True)
    if threshold is None:
        thresh = threshold_otsu(ref_imu)
    else:
        thresh = float(threshold)
    processed = ref_imu >= thresh
    
    # binary opening / closing
    if bin_opening is not None:
        el = disk(bin_opening*upscale)
        processed = binary_opening(processed, el)
    if bin_closing is not None:
        el = disk(bin_closing*upscale)
        processed = binary_closing(processed, el)

    # smooth and downscale
    processed = sp.ndimage.filters.gaussian_filter(processed*1.0, edge_sigma*upscale)
    processed = sp.ndimage.interpolation.zoom(processed, zoom=1.0/upscale,
                                              output=None, order=3,
                                              mode='constant', cval=0.0,
                                              prefilter=True)

    # scale mag
    mag_scale = np.percentile(im[processed>0.5], 50)
    processed = processed*mag_scale
    
    if aperture is not None and crop_pad:
        im_pad = np.zeros_like(image, dtype=float)
        im_pad[ri:rf+1, ci:cf+1] = im
        im = im_pad
        
        im_pad = np.zeros_like(image, dtype=float)
        im_pad[ri:rf+1, ci:cf+1] = processed
        processed = im_pad

    # plot
    if plot:
        err = processed-im
        pct = 0.1
        vmin_max = np.percentile(err, [pct, 100-pct])
        vmin, vmax = np.abs(vmin_max).max() * np.array([-1, 1])
        if widget is not None:
            docked = widget.setup_docking("", "Top", figsize=(9,3))
            fig = docked.get_fig()
            fig.clf()
            ax1, ax2, ax3 = fig.subplots(1, 3, sharex=True, sharey=True)
            f = fig.canvas
        else:
            f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(9,3))
        ax1.imshow(im)
        ax2.imshow(processed)
        ax3.imshow(err, vmin=vmin, vmax=vmax, cmap='bwr')
        ax1.set_title('Original')
        ax2.set_title('Processed')
        ax3.set_title('Processed : Original\n%0.3f - %0.3f' %(vmin_max[0], vmin_max[1]))
    
    return processed
