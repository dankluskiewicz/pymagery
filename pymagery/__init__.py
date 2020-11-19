import warnings
import numpy as np
from osgeo import gdal
import affine
import matplotlib.pyplot as plt
gdal.UseExceptions()

print('init raster')


class Raster:

    dflt_bands = {'dflt': np.array([[1, 0], [0, 1]])}

    def __init__(self, crs=None, aff=None, bands=dflt_bands, ):
        self._crs = None  # to keep track of when crs isn't set
        self._aff = None
        self.crs = crs
        self.aff = aff
        self.bands = bands

    def from_path(path):
        gdal_ds = gdal.Open(path)
        n_bands = gdal_ds.RasterCount
        if n_bands == 1:
            gdal_band = gdal_ds.GetRasterBand(1)
            arr = gdal_band.ReadAsArray()
            raster = SingleBand(bands={0: arr})
        else:
            bands = {i: gdal_ds.GetRasterBand(i+1).ReadAsArray()
                     for i in range(n_bands)}
            raster = MultiBand(bands=bands)
        raster.aff = affine.Affine(*gdal_ds.GetGeoTransform())
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
        # make sure all bands have same dimensions
        dims = set(arr.shape for arr in bands.values())
        if len(dims) != 1:
            raise Exception(f'inconsistent band dims: {dims}')
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

    dflt_bands = {'dflt': np.array([[1, 0], [0, 1]])}

    def __init__(self, bands=dflt_bands, **kwargs):
        super().__init__(bands=bands, **kwargs)
        assert len(self.bands) == 1
        self.arr = list(self.bands.values())[0]

    def plot(self, **kwargs):
        fig, ax = super().plot(**kwargs)
        ax.imshow(self.arr, **kwargs)
        return fig, ax


class MultiBand(Raster):
    dflt_bands = {'1': np.array([[1, 0], [0, 1]]),
                  '2': np.array([[0, 1], [1, 0]])}

    def plot(self):
        warnings.warn('can only plot one band at a time')

    def __init__(self, bands=dflt_bands, **kwargs):
        super().__init__(bands=bands, **kwargs)


class RGB(MultiBand):
    dflt_bands = {'r': np.array([[1, 0], [0, 1]]),
                  'g': np.array([[0, 1], [1, 0]]),
                  'b': np.array([[0, 0], [1, 1]])}

    def __init__(self):
        super().__init__(bands=bands, **kwargs)
        assert len(self.bands) == 3

    def plot(self, **kwargs):
        fig, ax = super().plot(**kwargs)
