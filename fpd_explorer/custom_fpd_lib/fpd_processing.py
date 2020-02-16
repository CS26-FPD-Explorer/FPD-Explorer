import fpd.fpd_processing as fpdp
import numpy as np
from tqdm import tqdm
from skimage.feature import canny,peak_local_max
from skimage.transform import hough_circle
from skimage.draw import circle_perimeter
from skimage import color
from skimage.feature import register_translation
from skimage.filters import threshold_otsu
from skimage.morphology import disk, binary_closing, binary_opening
from scipy.ndimage.filters import gaussian_filter, gaussian_filter1d
import matplotlib.pyplot as plt
import multiprocessing as mp
import sys
from functools import partial
import scipy as sp

def sum_im(data, nr, nc, mask=None, nrnc_are_chunks=False, progress_callback=None):
    '''
    Return a real-space sum image from data. 

    Parameters
    ----------
    data : array_like
        Mutidimensional fpd data of shape (scanY, scanX, ..., detY, detX).
    nr : integer or None
        Number of rows to process at once (see Notes).
    nc : integer or None
        Number of columns to process at once (see Notes).
    mask : 2-D array or None
        Mask is applied to data before taking sum.
        Shape should be that of the detector.
    nrnc_are_chunks : bool
        If True, `nr` and `nc` are interpreted as the number of chunks to
        process at once. If `data` is not chunked, `nr` and `nc` are used
        directly.
    progress_callback : CustomSignals
        If set, show the progress on the widget bar instead

    Returns
    -------
    Array of shape (scanY, scanX, ...).

    Notes
    -----
    If `nr` or `nc` are None, the entire dimension is processed at once.
    For chunked data, setting `nrnc_are_chunks` to True, and `nr` and `nc`
    to a suitable values can improve performance.


    '''

    if nrnc_are_chunks:
        nr, nc = fpdp._condition_nrnc_if_chunked(data, nr, nc, True)

    nondet = data.shape[:-2]
    nonscan = data.shape[2:]
    scanY, scanX = data.shape[:2]
    detY, detX = data.shape[-2:]

    r_if, c_if = fpdp._block_indices((scanY, scanX), (nr, nc))
    if mask is not None:
        for i in range(len(nondet)):
            mask = np.expand_dims(mask, 0)
            # == mask = mask[None,None,None,...]

    sum_im = np.empty(nondet)
    total_ims = np.prod(nondet)
    with tqdm(total=total_ims, mininterval=0, leave=True, unit='images') as pbar:
        for i, (ri, rf) in enumerate(r_if):
            for j, (ci, cf) in enumerate(c_if):
                if mask is None:
                    d = data[ri:rf, ci:cf, ...]
                else:
                    d = (data[ri:rf, ci:cf, ...] * mask)
                sum_im[ri:rf, ci:cf, ...] = d.sum((-2, -1))
                if progress_callback:
                    progress_callback.emit((np.prod(d.shape[:-2]), "sum_im"))
                else:
                    pbar.update(np.prod(d.shape[:-2]))

    print('\n')
    return sum_im


# --------------------------------------------------
def sum_dif(data, nr, nc, mask=None, nrnc_are_chunks=False, progress_callback=None):
    '''
    Return a summed diffraction image from data. 

    Parameters
    ----------
    data : array_like
        Mutidimensional fpd data of shape (scanY, scanX, ..., detY, detX).
    nr : integer or None
        Number of rows to process at once (see Notes).
    nc : integer or None
        Number of columns to process at once (see Notes).
    mask : array-like or None
        Mask applied to data before taking sum.
        Shape should be that of the scan.
    nrnc_are_chunks : bool
        If True, `nr` and `nc` are interpreted as the number of chunks to
        process at once. If `data` is not chunked, `nr` and `nc` are used
        directly.
    progress_callback : CustomSignals
        If set, show the progress on the widget bar instead

    Returns
    -------
    Array of shape (..., detY, detX).

    Notes
    -----
    If `nr` or `nc` are None, the entire dimension is processed at once.
    For chunked data, setting `nrnc_are_chunks` to True, and `nr` and `nc`
    to a suitable values can improve performance.

    '''

    if nrnc_are_chunks:
        nr, nc = fpdp._condition_nrnc_if_chunked(data, nr, nc, True)

    nondet = data.shape[:-2]
    nonscan = data.shape[2:]
    scanY, scanX = data.shape[:2]
    detY, detX = data.shape[-2:]

    r_if, c_if = fpdp._block_indices((scanY, scanX), (nr, nc))
    if mask is not None:
        for i in range(len(nonscan)):
            mask = np.expand_dims(mask, -1)
            # == mask = mask[..., None,None,None]

    sum_dif = np.zeros(nonscan)
    print('Calculating diffraction sum images.')
    total_ims = np.prod(nondet)
    with tqdm(total=total_ims, mininterval=0, leave=True, unit='images') as pbar:
        for i, (ri, rf) in enumerate(r_if):
            for j, (ci, cf) in enumerate(c_if):
                d = data[ri:rf, ci:cf, ...]
                d = np.ascontiguousarray(d)
                if mask is not None:
                    d = d * mask
                sum_dif += d.sum((0, 1))
                if progress_callback:
                    progress_callback.emit((np.prod(d.shape[:-2]), "sum_diff"))
                else:
                    pbar.update(np.prod(d.shape[:-2]))

    print('\n')
    return sum_dif

#--------------------------------------------------

def find_circ_centre(im, sigma, rmms, mask=None, plot=True, spf=1, low_threshold=0.1,
                     high_threshold=0.95, pct=None, max_n=1, widget = None):
    '''
    Find centre and radius of circle in image. Sub-pixel accurate with spf>1.
    
    Parameters
    ----------
    im : 2-D array
        Image data.
    sigma : scalar
        Smoothing width for canny edge detection .
    rmms : length 3 iterable
        Radius (min, max, step) in pixels.
    mask : array-like or None
        Mask for canny edge detection. False values are ignored.
        If None, no mask is applied.
    plot : bool
        Determines if best matching circle is plotted in matplotlib.
    spf : integer
        Sub-pixel factor. 1 for none. 
        If not None, step is forced to 1 and corresponds to 1/spf pixels.
    low_threshold : float
        Lower bound for hysteresis thresholding (linking edges) in [0, 1].
    high_threshold : float
        Upper bound for hysteresis thresholding (linking edges) in [0, 1].
    pct : None or scalar
        If not None, values in the image below this percentile are masked.
    max_n : int
        Maximum number of discs to find.
    widget : QtWidget
        A qt widget that must contain as many widgets or dock widget as there is popup window



    Returns
    -------
    Tuple of arrays of (center_y, center_x), radius.
    
    Notes
    -----
    Image is first scaled to full range of dtype, then upscaled if chosen.
    Canny edge detection is performed, followed by a Hough transform.
    Linking of edges is set by thresholds. See skimage.feature.canny for
    details. The best matching circle or circles are returned depending
    on the value of `max_n`.
    
    When multiple discs are present, increasing `high_threshold` reduces the
    number of edges considered  to those which higher connectivity. For bright
    field discs in STEM, values around 0.99 often work well.
    
    Examples
    --------
    Two calls can be made to make subpixel calculations efficient by 
    reducing the range over which the Hough transform takes place.
    
    >>> import fpd.fpd_processing as fpdp
    >>> from fpd.synthetic_data import disk_image
    
    >>> im = disk_image(intensity=64, radius=32)
    >>> rmms = (10, 100, 2)
    >>> spf = 1
    >>> sigma = 2
    >>> cyx, r = fpdp.find_circ_centre(im, sigma, rmms, mask=None, plot=True, spf=spf)
    
    >>> rmms = (r-4, r+4, 1)
    >>> spf = 4
    >>> cyx, r = fpdp.find_circ_centre(im, sigma, rmms, mask=None, plot=True, spf=spf)
    
    '''
    
    #TODO
    #decision on best centre, improved?
    #subpixel by 2-d gaussian fitting to hough space?
    
    ## scale im so default thresholding works appropriately (% of range)
    #im = (im.astype(np.float)/im.max()*np.iinfo(im.dtype).max)
    #im = im.astype(im.dtype)
    im = im.astype(float)
    
    if pct is not None:
        pct = np.percentile(im, pct)
        pct_mask = (im > pct).astype(bool)
        
        if mask is None:
            mask = pct_mask
        else:
            mask = np.logical_and(pct_mask, mask)
    
    if spf > 1:
        spf = float(spf)
        im = sp.ndimage.interpolation.zoom(im,
                                           spf,
                                           output=None,
                                           order=1,
                                           mode='reflect',
                                           prefilter=True)
        if mask is not None:
            mask = sp.ndimage.interpolation.zoom(mask*1.0,
                                                 spf,
                                                 output=None,
                                                 order=1,
                                                 mode='reflect',
                                                 prefilter=True)
            mask = mask > 0.5
        rmms = [x*spf for x in rmms[:2]] + [1]
    
    if plot:
        kwd = dict(adjustable='box-forced', aspect='equal')
        
        import matplotlib as mpl
        mplv = mpl.__version__
        from distutils.version import LooseVersion
        if LooseVersion(mplv) >= LooseVersion('2.2.0'):
           _ = kwd.pop('adjustable') 
        if widget is not None:
            docked = widget.setup_docking("Circular Center", "Bottom")
            fig = docked.get_fig()
            fig.clf()
            (ax1, ax2, ax3) = fig.subplots(1, 3, sharex=True, sharey=True,
                                          subplot_kw=kwd)
            f = fig.canvas

        else:
            f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, sharey=True,
                                          subplot_kw=kwd, figsize=(8,3))
        # plot image
        ax1.imshow(im, interpolation='nearest', cmap='gray')#,
                    #norm=mpl.colors.LogNorm())
        ax1.set_title('Image')

    edges = canny(im, sigma, mask=mask, use_quantiles=True,
                  low_threshold=low_threshold,
                  high_threshold=high_threshold)
    if plot:
        ax2.imshow(edges, interpolation='nearest', cmap='gray')
        ax2.set_title('Edges')


    # hough transform
    hough_radii = np.arange(rmms[0], rmms[1], rmms[2])
    hough_res = hough_circle(edges, hough_radii)

    centers = []
    accums = []
    radii = []
    for radius, h in zip(hough_radii, hough_res):
        peaks = peak_local_max(h, num_peaks=max_n)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * len(peaks))
    centers = np.array(centers)
    radii = np.array(radii)
    
    accum_order = np.argsort(accums)[::-1]
    idx = accum_order[:max_n]
    
    center_y, center_x = centers[idx].T
    radius = radii[idx].astype(int)
    
    if plot:
        # Draw the most prominent max_n circles
        imc = color.gray2rgb(im/im.max())
        for cyi, cxi, ri in zip(center_y, center_x, radius):
            cy, cx = circle_perimeter(cyi, cxi, ri)
            imc[cy, cx] = (1, 0, 0)
            imc[cyi, cxi] = (0, 1, 0)
        ax3.imshow(imc, interpolation='nearest')
        ax3.set_title('Detected Circle(s)')
        if widget is None:
            plt.draw()
        else:
            docked.get_canvas().draw()
            
    
    if spf > 1:
        center_y, center_x, radius = center_y/spf, center_x/spf, radius/spf
    
    return np.squeeze(np.array((center_y, center_x))).T, np.squeeze(radius)


def center_of_mass(data, nr, nc, aperture=None, pre_func=None, thr=None,
                   rebin=None, parallel=True, ncores=None, print_stats=True,
                   nrnc_are_chunks=False, origin='top', widget=None):
    '''
    Calculate a centre of mass image from fpd data. The results are
    naturally sub-pixel resolution.
    
    Parameters
    ----------
    data : array_like
        Mutidimensional data of shape (scanY, scanX, ..., detY, detX).
    nr : integer or None
        Number of rows to process at once (see Notes).
    nc : integer or None
        Number of columns to process at once (see Notes).
    aperture : array_like
        Mask of shape (detY, detX), applied to diffraction data after
        `pre_func` processing. Note, the data is automatically cropped
        according to the mask for efficiency.
    pre_func : callable
        Function that operates (out-of-place) on data before processing.
        out = pre_func(in), where in is nd_array of shape (n, detY, detX).
    thr : object
        Control thresholding of difraction image.
        If None, no thresholding.
        If scalar, threshold value.
        If string, 'otsu' for otsu thresholding.
        If callable, function(2-D array) returns thresholded image.
    rebin : integer or None
        Rebinning factor for detector dimensions. None or 1 for none. 
        If the value is incompatible with the cropped array shape, the
        nearest compatible value will be used instead. 
    parallel : bool
        If True, calculations are multiprocessed.
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
    widget : QtWidget
        A qt widget that must contain as many widgets or dock widget as there is popup window

    Returns
    -------
    Array of shape (yx, scanY, scanX, ...).
    Increasing Y, X CoM is disc shift up, right in image.
    
    Notes
    -----
    The order of operations is rebinning, pre_func, threshold, aperture,
    and CoM.
    
    If `nr` or `nc` are None, the entire dimension is processed at once.
    For chunked data, setting `nrnc_are_chunks` to True, and `nr` and `nc`
    to a suitable values can improve performance.
    
    The execution of pre_func is not multiprocessed, so it could employ 
    multiprocessing for cpu intensive calculations.
    
    Multiprocessing runs at a similar speed as non parallel code
    in the simplest case.
    
    Examples
    --------
    Using an aperture and rebinning:
    
    >>> import numpy as np
    >>> import fpd.fpd_processing as fpdp
    >>> from fpd.synthetic_data import disk_image, fpd_data_view
    
    >>> radius = 32
    >>> im = disk_image(intensity=1e3, radius=radius, size=256, upscale=8, dtype='u4')
    >>> data = fpd_data_view(im, (32,)*2, colours=0)
    >>> ap = fpdp.synthetic_aperture(data.shape[-2:], cyx=(128,)*2, rio=(0, 48), sigma=0, aaf=1)[0]
    >>> com_y, com_x = fpdp.center_of_mass(data, nr=9, nc=9, rebin=3, aperture=ap)
    
    
    '''
    
    # Possible alternative was not as fast in tests:
    # from scipy.ndimage.measurements import center_of_mass
    
    if nrnc_are_chunks:
        nr, nc = fpdp._condition_nrnc_if_chunked(data, nr, nc, print_stats)
        
    if ncores is None:
        ncores = mp.cpu_count()
    
    nondet = data.shape[:-2]
    nonscan = data.shape[2:]
    scanY, scanX = data.shape[:2]
    detY, detX = data.shape[-2:]
    
    use_ap = False
    if isinstance(aperture, np.ndarray):
        # determine limits to index array for efficiency
        rii, rif = np.where(aperture.sum(axis=1) > 0)[0][[0, -1]]
        cii, cif = np.where(aperture.sum(axis=0) > 0)[0][[0, -1]]
        use_ap = True
    else:
        rii, rif = 0, detY-1
        cii, cif = 0, detX-1
    data_square_len = rif-rii+1
    
    # TODO: the following is very similar to _parse_crop_rebin, except it operates
    # only on rii etc These could be refactored and combined to simplify.
    # rebinning
    rebinf = 1
    rebinning = rebin is not None and rebin != 1
    if rebinning:
        # change crop
        extra_pixels = int(np.ceil(data_square_len/float(rebin))*rebin) - data_square_len
        ext_pix_pads = extra_pixels // 2
        
        # this is where the decision on if extra pixels can be added and where 
        # they should go could be made
        if extra_pixels % 2:
            # odd
            ext_pix_pads = (-ext_pix_pads, ext_pix_pads+1)
        else:
            # even
            ext_pix_pads = (-ext_pix_pads, ext_pix_pads)
        riic, rifc = rii + ext_pix_pads[0], rif + ext_pix_pads[1]
        ciic, cifc = cii + ext_pix_pads[0], cif + ext_pix_pads[1]
        if riic < 0 or rifc > detY-1 or ciic < 0 or cifc > detX-1:
            # change rebin
            f, fs = fpdp._find_nearest_int_factor(data_square_len, rebin)
            if rebin != f:
                if print_stats:
                    print('Image data cropped to:', fpdp.cropped_im_shape)
                    print('Requested rebin (%d) changed to nearest value: %d. Possible values are:' %(rebin, f), fs)
                rebin = f
        else:
            rii, rif = riic, rifc
            cii, cif = ciic, cifc
            cropped_im_shape = (rif+1-rii, cif+1-cii)
            if print_stats:
                print('Image data cropped to:', cropped_im_shape)
        rebinf = rebin
    
    if use_ap:
        aperture = aperture[rii:rif+1, cii:cif+1].astype(np.float)
        if rebinning:
            ns = tuple([int(x/rebin) for x in aperture.shape])
            aperture = fpdp.rebinA(aperture, *ns)
    

    r_if, c_if = fpdp._block_indices((scanY, scanX), (nr, nc))
    com_im = np.zeros(nondet + (2,), dtype=np.float)
    yi, xi = np.indices((detY, detX))
    yi = yi[::-1, ...]   # reverse order so increasing Y is up.
    
    yixi = np.concatenate((yi[..., None], xi[..., None]), 2)
    yixi = yixi[rii:rif+1, cii:cif+1, :].astype(np.float)
    if rebinning:
        ns = tuple([int(x/rebin) for x in yixi.shape[:2]]) + yixi.shape[2:]
        yixi = fpdp.rebinA(yixi, *ns)
    yi0 = yixi[:, 0, 0]
    xi0 = yixi[0, :, 1]
    
    if print_stats:
        print('Calculating centre-of-mass')
        tqdm_file = sys.stderr
    else:
        tqdm_file = fpdp.DummyFile()
    total_nims = np.prod(nondet)
    with tqdm(total=total_nims, file=tqdm_file, mininterval=0, leave=True, unit='images') as pbar:
        for i, (ri, rf) in enumerate(r_if):
            for j, (ci, cf) in enumerate(c_if):               
                d = data[ri:rf, ci:cf, ..., rii:rif+1, cii:cif+1]#.astype(np.float)
                d = np.ascontiguousarray(d)
                if rebinning:
                    ns = d.shape[:-2] + tuple([int(x/rebin) for x in d.shape[-2:]])
                    d = fpdp.rebinA(d, *ns)
                
                # modify with function
                if pre_func is not None:
                    d = pre_func(d.reshape((-1,)+d.shape[-2:]))
                    d.shape = ns
                
                partial_comf = partial(fpdp._comf, 
                                    use_ap=use_ap, 
                                    aperture=aperture, 
                                    yi0=yi0,
                                    xi0=xi0, 
                                    thr=thr)
                
                d_shape = d.shape   # scanY, scanX, ..., detY, detX
                d.shape = (np.prod(d_shape[:-2]),) + d_shape[-2:]   
                # (scanY, scanX, ...), detY, detX
                
                if parallel:
                    pool = mp.Pool(processes=ncores)
                    rslt = pool.map(partial_comf, d)
                    pool.close()
                else:
                    rslt = list(map(partial_comf, d))
                rslt = np.asarray(rslt)
                
                #print(d_shape, com_im[ri:rf,ci:cf,...].shape, rslt.shape)
                rslt.shape = d_shape[:-2]+(2,)
                com_im[ri:rf, ci:cf, ...] = rslt
                pbar.update(np.prod(d.shape[:-2]))
    if print_stats:
        print('\n')
    com_im = (com_im)/rebinf**2 
    
    # roll: (scanY, scanX, ..., yx) to (yx, scanY, scanX, ...) 
    com_im = np.rollaxis(com_im, -1, 0)
    
    # default origin implementation is bottom
    if origin.lower() == 'top':
        com_im[0] = nonscan[0]-1 - com_im[0]
    
    # print some stats
    if print_stats:
        fpdp._print_shift_stats(com_im)
    
    return com_im

#--------------------------------------------------

def synthetic_aperture(shape, cyx, rio, sigma=1, dt=np.float, aaf=3, ds_method='rebin', norm=True):
    '''
    Create circular synthetic apertures. Sub-pixel accurate with aaf>1.
    
    Parameters
    ----------
    shape : length 2 iterable
        Image data shape (y,x).
    cyx : length 2 iterable
        Centre y, x pixel cooridinates
    rio : 2d array or length n itterable
        Inner and outer radii [ri,ro) in a number of forms.
        If a length n itterable and not 2d array, n-1 apertures are returned.
        If a 2d array of shape nx2, rio are taken from rows.
    sigma : scalar
        Stdev of Gaussian filter applied to aperture.
    dt : datatype
        Numpy datatype of returned array. If integer type, data is scaled.
    aaf : integer
        Anti-aliasing factor. Use 1 for none.
    ds_method : str
        String controlling the downsampling method. Methods are:
        'rebin'  for rebinning the data.
        'interp' for interpolation.
    norm : bool
        Controls normalisation of actual to ideal area. 
        For apertures extending beyond the image border, the value is 
        increase to give the same 'volume'.
    
    Returns
    -------
    Array of shape (n_ap, y, x).
    
    Notes
    -----
    Some operations may be more efficient if dt is of the same type as 
    the data to which it will be applied.
    
    Examples
    --------
    >>> import fpd.fpd_processing as fpdp
    >>> import matplotlib.pyplot as plt
    >>> plt.ion()
    
    >>> aps = fpdp.synthetic_aperture((256,)*2, (128,)*2, np.linspace(32, 192, 10))
    >>> _ = plt.matshow(aps[0])
    
    '''
    
    assert type(aaf) == int
    
    ds_methods = ['rebin', 'interp']
    ds_method = ds_method.lower()
    if ds_method not in ds_methods:
        erm = "'ds_method' must be one of: " + ', '.join(ds_methods)
        raise NotImplementedError(erm)
    im_shape = shape
    
    if type(rio) == np.ndarray and rio.ndim == 2:
        n = rio.shape[0]
    else:
        n = len(rio)-1
        rio = list(zip(rio[:-1], rio[1:]))
    
    m = np.ones((n,)+shape, dtype=dt)
    
    # prepare boolean edge selection
    yi, xi = np.indices(shape)
    ri = ((xi-cyx[1])**2 + (yi-cyx[0])**2)**0.5
    yb = np.logical_or(yi == 0, yi == shape[0]-1)
    xb = np.logical_or(xi == 0, xi == shape[1]-1)
    bm = np.logical_or(xb, yb)    
    ri_edge = ri[bm]
    ri_min = ri_edge.min()
    
    cy, cx = [t*aaf for t in cyx]
    shape = tuple([t*aaf for t in shape])
    y, x = np.indices(shape)
    sigma *= aaf
    
    for i, rio in enumerate(rio):
        ri, ro = [t*aaf for t in rio]
        r = np.sqrt((x - cx)**2 + (y - cy)**2)
        mi = np.logical_and(r >= ri, r < ro)
        mi = gaussian_filter(mi.astype(np.float),
                             sigma, 
                             order=0,
                             mode='reflect')
        
        if np.issubdtype(dt, float):
            mi = mi.astype(dt)
        elif np.issubdtype(dt, 'uint'):
            mi = (mi/mi.max()*np.iinfo(dt).max).astype(dt)
        else:
            print("WARNING: dtype '%s' not supported!" %(dt))
            mi = np.ones(shape)*np.nan
        if aaf != 1:
            if ds_method == 'rebin':
                mi = fpdp.rebinA(mi, *im_shape)/ float(aaf**2)
            elif ds_method == 'interp':
                mi = sp.ndimage.interpolation.zoom(mi, 
                                                1.0/aaf, 
                                                output=None,
                                                order=1,
                                                mode='constant',
                                                cval=0.0,
                                                prefilter=True)
        # clip any values outside range coming from interpolation
        mi = mi.clip(0, 1)
        if norm:
            mi *= (np.pi*(ro**2-ri**2)/aaf**2)/mi.sum()     # normalisation
        elif rio[1] > ri_min:
            #warnings.simplefilter('always', UserWarning)
            #warnings.warn(('Apperture may extend beyond image.'
            #               +' Consider setting norm to False.')
            #               , UserWarning) 
            #warnings.filters.pop(0)
            print("WARNING: Aperture extends beyond image (max r = %0.1f). Consider setting norm to True. 'rio':" %(ri_min), rio)
        m[i, :, :] = mi
    return m
