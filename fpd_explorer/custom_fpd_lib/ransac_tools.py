import fpd.fpd_processing as fpdp
from skimage.measure.fit import BaseModel
from skimage.measure import ransac
import scipy as sp
import numpy as np
from scipy.interpolate import SmoothBivariateSpline
from scipy.interpolate import UnivariateSpline
from tqdm import tqdm
from fpd.utils import seq_image_array, unseq_image_array
from fpd import ransac_tools as rt 

def ransac_im_fit(im, mode=1, residual_threshold=0.1, min_samples=10,
                  max_trials=1000, model_f=None, p0=None, mask=None,
                  scale=False, fract=1, param_dict=None, plot=False,
                  axes=(-2, -1), widget=None):
    '''
    Fits a plane, polynomial, convex paraboloid, arbitrary function, or
    smoothing spline to an image using the RANSAC algorithm.

    Parameters
    ----------
    im : ndarray
        ndarray with images to fit to.
    mode : integer [0-4]
        Specifies model used for fit.
        0 is function defined by `model_f`.
        1 is plane.
        2 is quadratic.
        3 is concave paraboloid with offset.
        4 is smoothing spline.
    model_f : callable or None
        Function to be fitted.
        Definition is model_f(p, *args), where p is 1-D iterable of params
        and args is iterable of (x, y, z) arrays of point cloud coordinates.
        See examples.
    p0 : tuple
        Initial guess of fit params for `model_f`.
    mask : 2-D boolean array
        Array with which to mask data. True values are ignored.
    scale : bool
        If True, `residual_threshold` is scaled by stdev of `im`.
    fract : scalar (0, 1]
        Fraction of data used for fitting, chosen randomly. Non-used data
        locations are set as nans in `inliers`.
    residual_threshold : float
        Maximum distance for a data point to be classified as an inlier.
    min_samples : int or float
        The minimum number of data points to fit a model to.
        If an int, the value is the number of pixels.
        If a float, the value is a fraction (0.0, 1.0] of the total number of pixels.
    max_trials : int, optional
        Maximum number of iterations for random sample selection.
    param_dict : None or dictionary.
        If not None, the dictionary is passed to the model estimator.
        For arbitrary functions, this is passed to scipy.optimize.leastsq.
        For spline fitting, this is passed to scipy.interpolate.SmoothBivariateSpline.
        All other models take no parameters.
    plot : bool
        If True, the data, including inliers, model, etc are plotted.
    axes : length 2 iterable
        Indices of the input array with images.
    widget : QtWidget
        A qt widget that must contain as many widgets or dock widget as there is popup window

    Returns
    -------
    Tuple of fit, inliers, n, where:
    fit : 2-D array
        Image of fitted model.
    inliers : 2-D array
        Boolean array describing inliers.
    n : array or None
        Normal of plane fit. `None` for other models.

    Notes
    -----
    See skimage.measure.ransac for details of RANSAC algorithm.

    `min_samples` should be chosen appropriate to the size of the image
    and to the variation in the image.

    Increasing `residual_threshold` increases the fraction of the image
    fitted to.

    The entire image can be fitted to without RANSAC by setting:
    max_trials=1, min_samples=1.0, residual_threshold=`x`, where `x` is a
    suitably large value.

    Examples
    --------
    `model_f` for paraboloid with offset:

    >>> def model_f(p, *args):
    ...     (x, y, z) = args
    ...     m = np.abs(p[0])*((x-p[1])**2 + (y-p[2])**2) + p[3]
    ...     return m
    >>> p0 = (0.1, 10, 20, 0)


    To plot fit, inliers etc:

    >>> from fpd.ransac_tools import ransac_im_fit
    >>> import matplotlib as mpl
    >>> from numpy.ma import masked_where
    >>> import numpy as np
    >>> import matplotlib.pylab as plt
    >>> plt.ion()


    >>> cmap = mpl.cm.gray
    >>> cmap.set_bad('r')

    >>> image = np.random.rand(*(64,)*2)
    >>> fit, inliers, n = ransac_im_fit(image, mode=1)
    >>> cor_im = image-fit

    >>> pct = 0.5
    >>> vmin, vmax = np.percentile(cor_im, [pct, 100-pct])
    >>>
    >>> f, axs = plt.subplots(1, 4, sharex=True, sharey=True)
    >>> _ = axs[0].matshow(image, cmap=cmap)
    >>> _ = axs[1].matshow(masked_where(inliers==False, image), cmap=cmap)
    >>> _ = axs[2].matshow(fit, cmap=cmap)
    >>> _ = axs[3].matshow(cor_im, vmin=vmin, vmax=vmax)



    To plot plane normal vs threshold:

    >>> from fpd.ransac_tools import ransac_im_fit
    >>> from numpy.ma import masked_where
    >>> import numpy as np
    >>> from tqdm import tqdm
    >>> import matplotlib.pylab as plt
    >>> plt.ion()

    >>> image = np.random.rand(*(64,)*2)
    >>> ns = []
    >>> rts = np.logspace(0, 1.5, 5)
    >>> for rt in tqdm(rts):
    ...     nis = []
    ...     for i in range(64):
    ...         fit, inliers, n = ransac_im_fit(image, residual_threshold=rt, max_trials=10)
    ...         nis.append(n)
    ...     ns.append(np.array(nis).mean(0))
    >>> ns = np.array(ns)

    >>> thx = np.arctan2(ns[:,1], ns[:,2])
    >>> thy = np.arctan2(ns[:,0], ns[:,2])
    >>> thx = np.rad2deg(thx)
    >>> thy = np.rad2deg(thy)

    >>> _ = plt.figure()
    >>> _ = plt.semilogx(rts, thx)
    >>> _ = plt.semilogx(rts, thy)

    '''

    # Set model
    # Functions defining classes are needed to pass parameters since class must
    # not be instantiated or are monkey patched (only in spline implementation)
    if mode == 0:
        # generate model_class with passed function
        if p0 is None:
            raise NotImplementedError('p0 must be specified.')
        model_class = rt._model_class_gen(model_f, p0, param_dict)
    elif mode == 1:
        # linear
        model_class = rt._Plane3dModel
    elif mode == 2:
        # quadratic
        model_class = rt._Poly3dModel
    elif mode == 3:
        # concave paraboloid
        model_class = rt._Poly3dParaboloidModel
    elif mode == 4:
        # spline
        class _Spline3dModel_monkeypatched(_Spline3dModel):
            pass
        model_class = _Spline3dModel_monkeypatched
        model_class.param_dict = param_dict

    multiim = False
    if im.ndim > 2:
        multiim = True
        ims, unflat_shape = seq_image_array(im, axes)
        pbar = tqdm(total=ims.shape[0])
    else:
        ims = im[None]

    fits = []
    inlierss = []
    ns = []

    for imi in ims:
        # set data
        yy, xx = np.indices(imi.shape)
        zz = imi
        if mask is None:
            keep = (np.ones_like(imi) == 1).flatten()
        else:
            keep = (mask == False).flatten()
        data = np.column_stack([xx.flat[keep], yy.flat[keep], zz.flat[keep]])

        if type(min_samples) is int:
            # take number directly
            pass
        else:
            # take number as fraction
            min_samples = int(len(keep) * min_samples)
            print("min_samples is set to: %d" % (min_samples))

        # randomly select data
        sel = np.random.rand(data.shape[0]) <= fract
        data = data[sel.flatten()]

        # scale residual, if chosen
        if scale:
            residual_threshold = residual_threshold * np.std(data[:, 2])

        # determine if fitting to all
        full_fit = min_samples == data.shape[0]

        if not full_fit:
            # do ransac fit
            model, inliers = ransac(data=data,
                                    model_class=model_class,
                                    min_samples=min_samples,
                                    residual_threshold=residual_threshold,
                                    max_trials=max_trials)
        else:
            model = model_class()
            inliers = np.ones(data.shape[0]) == 1

        # get params from fit with all inliers
        model.estimate(data[inliers])
        # get model over all x, y
        args = (xx.flatten(), yy.flatten(), zz.flatten())
        fit = model.my_model(model.params, *args).reshape(imi.shape)

        if mask is None and fract == 1:
            inliers = inliers.reshape(imi.shape)
        else:
            inliers_nans = np.empty_like(imi).flatten()
            inliers_nans[:] = np.nan
            yi = np.indices(inliers_nans.shape)[0]

            sel_fit = yi[keep][sel.flatten()]
            inliers_nans[sel_fit] = inliers
            inliers = inliers_nans.reshape(imi.shape)

        # calculate normal for plane
        if mode == 1:
            # linear
            C = model.params
            n = np.array([-C[0], -C[1], 1])
            n_mag = np.linalg.norm(n, ord=None, axis=0)
            n = n / n_mag
        else:
            # non-linear
            n = None

        if plot:
            import matplotlib.pylab as plt
            import matplotlib as mpl
            from numpy.ma import masked_where
            from mpl_toolkits.axes_grid1 import ImageGrid

            plt.ion()
            cmap = mpl.cm.gray
            cmap.set_bad('r')

            cor_im = imi - fit
            pct = 0.1
            vmin, vmax = np.percentile(cor_im, [pct, 100 - pct])
            if widget is None:
                fig = plt.figure()
            else:
                docked = widget.setup_docking("Circular Center", "Bottom")
                fig = docked.get_fig()
                fig.clf()

            grid = ImageGrid(fig, 111,
                             nrows_ncols=(1, 4),
                             axes_pad=0.1,
                             share_all=True,
                             label_mode="L",
                             cbar_location="right",
                             cbar_mode="single")

            images = [imi, masked_where(inliers == False, imi), fit, cor_im]
            titles = ['Image', 'Inliers', 'Fit', 'Corrected']
            for i, image in enumerate(images):
                img = grid[i].imshow(image, cmap=cmap, interpolation='nearest')
                grid[i].set_title(titles[i])
            img.set_clim(vmin, vmax)
            grid.cbar_axes[0].colorbar(img)

            #f, axs = plt.subplots(1, 4, sharex=True, sharey=True)
            #_ = axs[0].matshow(imi, cmap=cmap)
            #_ = axs[1].matshow(masked_where(inliers==False, imi), cmap=cmap)
            #_ = axs[2].matshow(fit, cmap=cmap)
            #_ = axs[3].matshow(cor_im, vmin=vmin, vmax=vmax)

            # for i, title in enumerate(['Image' , 'Inliers', 'Fit', 'Corrected']):
            # axs[i].set_title(title)
            # plt.tight_layout()
        fits.append(fit)
        inlierss.append(inliers)
        ns.append(n)
        if multiim:
            pbar.update(1)
    fit = np.array(fits)
    inliers = np.array(inlierss)
    n = np.array(ns)

    if multiim:
        pbar.close()

        # reshape
        fit = unseq_image_array(fit, axes, unflat_shape)
        inliers = unseq_image_array(inliers, axes, unflat_shape)
        n = unseq_image_array(n, axes, unflat_shape)
    else:
        fit = fit[0]
        inliers = inliers[0]
        n = n[0]

    return (fit, inliers, n)
