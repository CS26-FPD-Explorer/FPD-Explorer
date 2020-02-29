import fpd
from fpd import fpd_processing as fpdp
from fpd import _p3
import sys
import multiprocessing as mp
import tqdm
import numpy as np
from . import fpd_processing as fpdp_new


def phase_correlation(data, nr, nc, cyx=None, crop_r=None, sigma=2.0,
                      spf=100, pre_func=None, post_func=None, mode='2d',
                      ref_im=None, rebin=None, der_clip_fraction=0.0,
                      der_clip_max_pct=99.9, truncate=4.0, parallel=True,
                      ncores=None, print_stats=True, nrnc_are_chunks=False, origin='top'):
    '''
    Perform phase correlation on 4-D data using efficient upscaling to
    achieve sub-pixel resolution.
    
    Parameters
    ----------
    data : array_like
        Mutidimensional data of shape (scanY, scanX, ..., detY, detX).
    nr : integer or None
        Number of rows to process at once (see Notes).
    nc : integer or None
        Number of columns to process at once (see Notes).
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
                    pool = mp.dummy.Pool(processes=ncores)
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
        fpdp_new.print_shift_stats(shift_yx)

    return shift_yx, shift_err, shift_difp, ref
