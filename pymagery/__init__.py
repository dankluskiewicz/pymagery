import warnings
import numpy as np
from osgeo import gdal
import rasterio
import rasterio.fill
import affine
import shapely
import shapely.geometry
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
from collections import UserDict
gdal.UseExceptions()


class Band(np.ndarray):
    '''
    a subclass of np.ndarray that will always have type float (this
    handles nodatas better), and has new methods to operate as part of
    a Raster class.
    '''

    def __new__(cls, input_array):
        if type(input_array) is Band:
            return input_array
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        band = np.asarray(input_array).astype(float).view(cls)
        # Finally, we must return the newly created object:
        return band

    def __array_finalize__(self, band):
        '''
        Necessary to subclass an ndarray. See numpy docs
        '''
        if band is None:
            return

    def fill_nans(self, val):
        '''
        fill nans w/ value <val>
        '''
        filled = self.copy()
        filled[np.isnan(filled)] = val
        return filled

    def fill_negs(self, val):
        '''
        fill nans w/ value <val>
        '''
        filled = self.copy()
        filled[filled < 0] = val
        return filled

    def interp(self):
        '''
        replace np.nan values w/ spline interpolation
        '''
        mask = self.fill_nans(0)
        filled = self.copy()
        filled = rasterio.fill.fillnodata(filled, mask=mask)
        return filled


class Bands(UserDict):
    """
    This will behave like a dict, except that its values will automatically
    convert to type Band and it has a method for calling values (bands)
    by order
    """

    def __init__(self, *args, **kwargs):
        # make sure that all the contents are of type Band
        super().__init__(*args, **kwargs)
        # for i, band in self.items():
        #     self[i] = Band(band)

    def get_ith(self, i):
        # for calling bands by order
        if type(i) in (int, np.int64):
            return list(self.values())[i]
        if type(i) is slice:
            sl = i
            print(sl)
            idx = np.arange(*(x for x in (sl.start, sl.stop, sl.step) if x))
            return np.array([self.get_ith(i) for i in idx if i < len(self)])

    def __setitem__(self, i, band):
        super().__setitem__(i, Band(band))


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
            bands = Bands({str(i): gdal_ds.GetRasterBand(i + 1).ReadAsArray()
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
            warnings.warn('changing raster crs w/o transformation',
                          UserWarning)
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

    @property
    def dx(self):
        return self.aff.a

    @property
    def dy(self):
        return self.aff.e

    @property
    def shape(self):
        return self.bands.get_ith(0).shape

    @property
    def N(self):
        return self.shape[0]

    @property
    def M(self):
        return self.shape[1]

    def plot(self, ax=None, figsize=(8, 8)):
        # this just sets up a fig if the user didn't already do so
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            return fig, ax
        return None, ax

    @property
    def bounds(self):
        """
        :return:
        x_min, y_min, x_max, y_max
        """
        n, m = self.shape
        x_min, y_max = self.aff * (0, 0)
        x_max, y_min = self.aff * (m, n)
        bounds = (x_min, y_min, x_max, y_max)
        return bounds

    @property
    def plotting_extent(self):
        x_min, y_min, x_max, y_max = self.bounds
        return (x_min, x_max, y_min, y_max)

    @property
    def bounding_box(self):
        x_min, y_min, x_max, y_max = self.bounds
        box = shapely.geometry.Polygon([
            (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max),
            (x_min, y_min)])
        return box

    def fill_nans(self, val=0):
        for key, band in self.bands.items():
            self.bands[key] = band.fill_nans(val)

    def fill_negs(self, val=0):
        for key, band in self.bands.items():
            self.bands[key] = band.fill_negs(val)

    def pix_to_geo(self, i, j):
        x, y = self.aff * (j, i)
        return x, y

    def geo_to_pix(self, x, y):
        j, i = (int(np.floor(i)) for i in ~self.aff * (x, y))
        return i, j


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
        if len(bands) != 1:
            raise Exception(
                f'cannot have single-band raster w/ {len(bands)} bands')
        if type(bands) is not Bands:
            bands = Bands(bands)
        self._bands = bands

    @property
    def arr(self):
        return list(self.bands.values())[0]

    @arr.setter
    def arr(self, arr):
        raise NotImplementedError('set band, not derived attr "arr"')

    def mk_hill_shade(self, cmap=plt.cm.gist_earth, azimuth=45, zenith=45):
        dx, dy = self.dx, self.dy
        z = self.arr.copy()
        # np.nan will throw things off
        if np.isnan(z).any():
            warnings.warn('nans in a raster will compromise a hillshade')
        ls = mpl.colors.LightSource(azdeg=315, altdeg=45)
        hs_arr = ls.shade(z, cmap=cmap, dx=dx, dy=dy)
        return hs_arr

    def plot(self, cbar_fig=None, ax=None, cmap=plt.cm.gist_earth,
             hs=False, **kwargs):
        """
        :param cbar_fig: (plt.figure) supply if you want a colorbar
        :param kwargs:
        :return:
        """
        fig, ax = super().plot(ax=ax)
        arr = self.arr
        if hs:
            arr = self.mk_hill_shade()
        im = ax.imshow(arr, extent=self.plotting_extent, cmap=cmap, **kwargs)
        if cbar_fig is not None:
            cbar_fig.colorbar(im, ax=ax, orientation='vertical', fraction=.1)
        return fig, ax


class MultiBand(Raster):

    def plot(self, **kwargs):
        warnings.warn('can only plot one band at a time')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def arr(self):
        """
        this is the bands reshaped for plt.imshow
        cached
        """
        if self._arr is None:
            self._arr = np.stack(list(self.bands.values()), axis=2)
        return self._arr


class RGB(MultiBand):

    def __init__(self, *args, **kwargs):
        """
        :param args: (MultiBand) use this to converts a MultiBand to an RGB
        :param kwargs: use this for standard Raster instantiation
        """
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

    def from_path(path):
        mb = MultiBand.from_path(path)
        rgb = RGB(mb)
        return rgb

    def plot(self, **kwargs):
        fig, ax = Raster.plot(self, **kwargs)
        ax.imshow(self.arr[:, :, :3], extent=self.plotting_extent)
        return fig, ax
