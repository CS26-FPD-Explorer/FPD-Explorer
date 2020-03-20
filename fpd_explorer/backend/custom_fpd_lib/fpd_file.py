import numpy as np

def get_memmap(self):
    '''
    Returns a memory mapped array for out-of-core data access. 
    Delete the memmap instance to close the file.
    
    Returns
    -------
    mm : numpy.core.memmap.memmap
        Memory mapped on-disk array. To close the file, delete the object
        with `del mm`.
    
    Examples
    --------
    >>> from fpd.fpd_file import MerlinBinary, DataBrowser  +SKIP
    >>> import numpy as np  +SKIP
    
    >>> mb = MerlinBinary(binary_filename, header_filename, dm_filename)    +SKIP
    
    >>> mm = mb.get_memmap()    +SKIP
    
    This may be plotted with a navigation image generated from the data:
    >>> nav_im = mm.sum((-2,-1))    +SKIP
    or a blank image:
    >>> nav_im = np.zeros(mm.shape[:2]) +SKIP
    >>> b = DataBrowser(mm, nav_im=nav_im)  +SKIP
    
    Notes
    -----
    Based on https://gitlab.com/fpdpy/fpd/issues/16#note_72345827
    
    '''
    
    self._memmap_check()
    
    header_pixels = self._Mbhp.header_bytesize // (self._Mbhp.bitdepth_bin // 8)
    image_pixels = self._detY * self._detX + header_pixels
    offset = self._ds_start_skip * (self._Mbhp.header_bytesize + self._im_bytesize)
    
    shape = list(self.shape)
    shape[1] = shape[1] + self._row_end_skip
    shape = shape[:-2] + [image_pixels]
    shape = tuple(shape)
    
    mm = np.memmap(self._binfns[0], dtype=self._det_dtype, mode="r+",
                    offset=offset, shape=shape)
    
    end_ind = -self._row_end_skip
    if end_ind == 0:
        end_ind = None
    mm = mm[:, :end_ind, ..., header_pixels:]
    # invert so origin is at top
    mm = mm.reshape(self.shape)[..., ::-1, :]
    return mm
