import pytest
import affine
import numpy as np


from pymagery import context
import pymagery


@pytest.fixture
def crs():
    return 'epsg:26911'


@pytest.fixture
def aff():
    return affine.Affine(1, 0, 10, 0, -1, 20)


@pytest.fixture
def arr():
    arr = np.array([[1, 0, 1, 2],
                    [0, 1, 0, 3],
                    [1, 0, 2, 4]], dtype=np.float64)
    return arr


@pytest.fixture
def arr_wit_nans(arr):
    wit_nans = arr
    wit_nans[0, :3] = np.nan
    return wit_nans


@pytest.fixture
def arr_wit_negs(arr):
    wit_negs = arr
    wit_negs[0, :3] = [-1, -99, -999]
    return wit_negs


@pytest.fixture
def arrs():
    return {1: np.array([[1, 0], [0, 1]]),
            2: np.array([[0, 1], [1, 0]])}


@pytest.fixture
def band(arr):
    return pymagery.Band(arr)


@pytest.fixture
def sb_bands(band):
    return pymagery.Bands({0: band})


@pytest.fixture
def mb_bands():
    return pymagery.Bands({1: pymagery.Band([[1, 0], [0, 1]]),
                           2: pymagery.Band([[0, 1], [1, 0]])})


@pytest.fixture
def rgb_bands():
    return pymagery.Bands({'r': pymagery.Band([[1, 0], [0, 1]]),
                           'g': pymagery.Band([[0, 1], [1, 0]]),
                           'b': pymagery.Band([[0, 0], [1, 1]])})


@pytest.fixture
def raster(sb_bands):
    return pymagery.Raster(bands=sb_bands)


@pytest.fixture
def sb(band, aff):
    return pymagery.SingleBand(band=band, aff=aff)


@pytest.fixture
def mb(mb_bands):
    return pymagery.MultiBand(bands=mb_bands, aff=aff)


@pytest.fixture
def rgb(rgb_bands):
    return pymagery.RGB(bands=rgb_bands, aff=aff)


@pytest.fixture
def dem():
    dem_path = context.dem_paths[0]
    return pymagery.SingleBand.from_path(dem_path)
