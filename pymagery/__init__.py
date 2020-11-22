import warnings
import numpy as np
from osgeo import gdal
import affine
import matplotlib.pyplot as plt
gdal.UseExceptions()

print('init raster')


class Bands(dict):
    """
    This will behave like a dict, except that bands[n]
    returns the nth item in the dict, and bands[:n] will return
    the first n items. I want to be able to
    label a single band with a string, but for many purposes
    it is useful to be able to call bands by order.
    """
    def __getitem__(self, i):
        if type(i) in (int, np.int64):
            return list(self.values())[i]
        if type(i) is slice:
            sl = i
            print(sl)
            idx = np.arange(*(x for x in (sl.start, sl.stop, sl.step) if x))
            print(idx)
            return np.array([self[i] for i in idx if i < len(self)])
        print(i, type(i))
        return super().__getitem__(i)


class Raster:
    """
    this is a base class for all raster types
    """

    def __init__(self, bands=None, crs=None, aff=None):
        self._crs = None  # to keep track of when crs isn't set
        self._aff = None
        self._bands = None
        self.crs = crs
        self.aff = aff
        self.bands = bands

    def from_path(path):
        """
        this will return a raster of type SingleBand or MultiBand
        """
        gdal_ds = gdal.Open(path)
        n_bands = gdal_ds.RasterCount
        if n_bands == 1:
            gdal_band = gdal_ds.GetRasterBand(1)
            arr = gdal_band.ReadAsArray()
            raster = SingleBand(bands=Bands({'0': arr}))
        else:
            bands = Bands({str(i): gdal_ds.GetRasterBand(i+1).ReadAsArray()
                     for i in range(n_bands)})
            raster = MultiBand(bands=bands)
        c, a, b, f, d, e = gdal_ds.GetGeoTransform()
        raster.aff = affine.Affine(a, b, c, d, e, f)
        raster.crs = gdal_ds.GetProjectionRef()
        return raster


    def from_paths(paths):
        pass

    @property
    def crs(self):
        return self._crs

    @crs.setter
    def crs(self, crs):
        if self.crs is not None:
            warnings.warn('changing raster crs w/o transformation')
        self._crs = crs

    @property
    def aff(self):
        return self._aff

    @aff.setter
    def aff(self, aff):
        if self.aff is not None:
            warnings.warn('changing raster aff w/o transformation')
        self._aff = aff

    @property
    def bands(self):
        return self._bands

    @bands.setter
    def bands(self, bands):
        """
        args:
            bands (dict of str: arr)
        """
        if bands is None:
            return
        # make sure all bands have same dimensions
        dims = set(arr.shape for arr in bands.values())
        if len(dims) != 1:
            raise Exception(f'inconsistent band dims: {dims}')
        if type(bands) is not Bands:
            bands = Bands(bands)
        self._bands = bands

    @property
    def n_bands(self):
        return len(self.bands)

    def plot(self, ax=None, figsize=(8, 8), **kwargs):
        # this just sets up a fig if the user didn't already do so
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            return fig, ax

    @property
    def bounds(self):
        """
        :return:
        x_min, y_min, x_max, y_max
        """
        n, m = self.shape
        x_min, y_max = (0, 0) * self.aff
        x_max, y_min = (m, n) * self.aff
        bounds = (x_min, y_min, x_max, y_max)
        return bounds

    @property
    def plotting_extent(self):
        x_min, y_min, x_max, y_max = self.bounds
        return (x_min, x_max, y_min, y_max)

    @property
    def shape(self):
        return self.bands[0].shape


class SingleBand(Raster):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def bands(self):
        return self._bands

    @bands.setter
    def bands(self, bands):
        if bands is None:
            return
        assert len(bands) == 1
        self._bands = bands

    @property
    def arr(self):
        return list(self.bands.values())[0]

    @arr.setter
    def arr(self, arr):
        raise NotImplementedError('set band, not derived attr "arr"')

    def plot(self, cbar_fig=None, **kwargs):
        """
        :param cbar_fig: (plt.figure) supply if you want a colorbar
        :param kwargs:
        :return:
        """
        fig, ax = super().plot(**kwargs)
        im = ax.imshow(self.arr, extent=self.plotting_extent, **kwargs)
        if cbar_fig is not None:
            cbar_fig.colorbar(im, ax=ax, orientation='vertical', fraction=.1)
        return fig, ax


class MultiBand(Raster):

    def plot(self, **kwargs):
        warnings.warn('can only plot one band at a time')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RGB(MultiBand):

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            # then convert from multi_band
            mb = args[0]
            super().__init__(bands=mb.bands, crs=mb.crs, aff=mb.aff)
        elif len(args) > 1:
            raise Exception('too many args for RGB()')
        else:
            super().__init__(**kwargs)
        self._arr = None

    @property
    def bands(self):
        return self._bands

    @bands.setter
    def bands(self, bands):
        if bands is None:
            return
        if len(bands) not in [3, 4]:
            raise ValueError(f'len input bands is {len(bands)}')
        # rename keys r, g, b
        new_bands = Bands()
        rgb_gen = (x for x in 'rgba')
        for val in bands.values():
            new_bands[next(rgb_gen)] = val
        self._bands = new_bands

    @property
    def arr(self):
        """
        this is the bands reshaped for plt.imshow
        cached
        """
        if self._arr is None:
            self._arr = np.stack(list(self.bands.values())[:3], axis=2)
        return self._arr




    def from_path(path):
        mb = MultiBand.from_path(path)
        rgb = RGB(mb)
        return rgb


    def plot(self, **kwargs):
        fig, ax = Raster.plot(self, **kwargs)
        ax.imshow(self.arr, extent=self.plotting_extent)
        return fig, ax
