import fpd.fpd_processing as fpdp
import numpy as np
from tqdm import tqdm


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
                    d = (data[ri:rf, ci:cf, ...]*mask)
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
                    d = d*mask
                sum_dif += d.sum((0, 1))
                if progress_callback:
                    progress_callback.emit((np.prod(d.shape[:-2]), "sum_diff"))
                else:
                    pbar.update(np.prod(d.shape[:-2]))

    print('\n')
    return sum_dif
