import pytest
import affine
import numpy as np


from . import context
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
def band(arr):
    return pymagery.Band(arr)


@pytest.fixture
def sb_bands(arr):
    return {0: arr}


@pytest.fixture
def mb_bands():
    return {1: np.array([[1, 0], [0, 1]]),
            2: np.array([[0, 1], [1, 0]])}


@pytest.fixture
def rgb_bands():
    return {'r': np.array([[1, 0], [0, 1]]),
            'g': np.array([[0, 1], [1, 0]]),
            'b': np.array([[0, 0], [1, 1]])}


@pytest.fixture
def raster(sb_bands):
    return pymagery.Raster(bands=sb_bands)


@pytest.fixture
def sb(sb_bands):
    return pymagery.SingleBand(bands=sb_bands, aff=aff)


@pytest.fixture
def mb(mb_bands):
    return pymagery.MultiBand(bands=mb_bands, aff=aff)


@pytest.fixture
def rgb(rgb_bands):
    return pymagery.RGB(bands=rgb_bands, aff=aff)
