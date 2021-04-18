import pymagery
import numpy as np
import pytest

from pymagery import context


def test_band_subsetting(arr, band):
    sub_band = band[:3, :3]
    assert type(sub_band is pymagery.Band)
    assert (sub_band == arr[:3, :3]).all()


def test_band_assigment(band):
    band[0, 0] = np.nan
    assert np.isnan(band[0, 0])


def test_band_fill_nans(arr, arr_wit_nans):
    band = pymagery.Band(arr_wit_nans)
    filled = band.fill_nans(9)
    # check on filled vals
    assert (filled[0, :3] == 9).all()
    # and check on the others
    assert (filled[1:] == arr[1:]).all()
    # check preservation
    np.testing.assert_equal(band, arr_wit_nans)


def test_band_fill_negs(arr, arr_wit_negs):
    band = pymagery.Band(arr_wit_negs)
    filled = band.fill_negs(9)
    # check on filled vals
    assert (filled[0, :3] == 9).all()
    # and check on the others
    assert (filled[1:] == arr[1:]).all()
    # check preservation
    assert (band == arr_wit_negs).all()


def test_band_interp(arr):
    arr[0, 0] = np.nan
    band = pymagery.Band(arr)
    interpd = band.interp()
    # preserve original?
    assert np.isnan(band[0, 0])
    # new value correct?
    neighbors = np.array([band[1, 0], band[0, 1], band[1, 1]])
    assert min(neighbors) <= interpd[0, 0] <= max(neighbors)


def test_bands_type_conversions(arrs):
    bands = pymagery.Bands(arrs)
    assert type(bands) is pymagery.Bands
    for band in bands.values():
        assert type(band) is pymagery.Band


def test_bands_iloc(sb_bands, mb_bands):
    for bands in (sb_bands, mb_bands):
        # make sure that you have access to the bands
        for i, key in enumerate(bands.keys()):
            assert (bands.iloc[i] == bands[key]).all()
        # and that you can modify them when accessed this way
        for i, key in enumerate(bands.keys()):
            band = bands.iloc[i]
            band[:, :] = 3
            assert (bands[key] == 3).all()


def test_raster_iloc(sb, mb):
    for raster in (sb, mb):
        # make sure that you have access to the bands
        for i, key in enumerate(raster.bands.keys()):
            assert (raster.iloc[i] == raster.bands[key]).all()
        # and that you can modify them when accessed this way
        for i, key in enumerate(raster.bands.keys()):
            band = raster.iloc[i]
            band[:, :] = 3
            assert (raster.bands[key] == 3).all()


def test_raster_init():
    raster = pymagery.Raster()


def test_single_band_init(sb, sb_bands):
    assert sb.bands == sb_bands


def test_multi_band_init(mb, mb_bands):
    pymagery.MultiBand()
    assert mb.bands == mb_bands


def test_rgb_init(rgb, rgb_bands):
    assert rgb.bands == rgb_bands
    assert list(rgb.bands.keys()) == ['r', 'g', 'b']


def test_aff(raster):
    aff = raster.aff


def test_set_aff(raster, aff):
    raster.aff = aff
    assert aff == raster.aff


def test_pix_geo_conversion(raster, aff):
    raster.aff = aff
    origin = (0, 0)
    xy_origin = raster.pix_to_geo(*origin)
    assert origin == raster.geo_to_pix(*xy_origin)


def test_crs(raster):
    crs = raster.crs


def test_set_crs(raster, crs):
    raster.crs = crs


def test_set_crs_again(raster, crs):
    # should result in a warning
    raster.crs = crs
    with pytest.warns(
            UserWarning,
            match='changing raster crs w/o transformation'):
        raster.crs = crs


def test_get_bands(raster, sb_bands):
    assert sb_bands == raster.bands


def test_set_bands(raster, mb_bands):
    raster.bands = mb_bands
    assert (mb_bands == raster.bands)


def test_set_bands_handles_arr_inputs(raster, arrs):
    raster.bands = arrs
    for band in raster.bands.values():
        if type(band) is not pymagery.Band:
            raise TypeError(f'band is type {type(band)}')


def test_raster_get_set_item(sb, mb):
    # get
    for raster in (sb, mb):
        for band_name, band in raster.bands.items():
            assert (raster[band_name] == band).all()
    # set
    for raster in (sb, mb):
        for band_name in raster.band_names:
            new_band = raster[band_name] + 1
            raster[band_name] = new_band
            assert (raster[band_name] == new_band).all()


def test_sb_arr(sb):
    arr = sb.arr
    print(arr)
    assert (arr == list(sb.bands.values())[0]).all()


def test_sb_minmax(sb):
    assert sb.min() == np.min(sb.arr)
    assert sb.max() == np.max(sb.arr)


def test_rgb_arr(rgb):
    arr = rgb.arr
    band_shape = list(rgb.bands.values())[0].shape
    assert arr.shape == (*band_shape, 3)


def test_copies(raster, sb, rgb, mb):
    assert raster.copy() == raster
    assert sb.copy() == sb
    assert rgb.copy() == rgb
    assert mb.copy() == mb


def test_sb_fill_nans(arr_wit_nans):
    sb = pymagery.SingleBand(band=arr_wit_nans)
    filled = sb.fill_nans(0)
    assert (filled.arr[0, :3] == 0).all()
    filled = sb.fill_nans(1)
    assert (filled.arr[0, :3] == 1).all()


def test_sb_fill_negs(arr_wit_negs):
    sb = pymagery.SingleBand(band=arr_wit_negs)
    filled = sb.fill_negs(0)
    assert (filled.arr[0, :3] == 0).all()
    filled = sb.fill_negs(1)
    assert (filled.arr[0, :3] == 1).all()


def test_mb_fill_nans(mb, arr_wit_nans):
    nan_locs = np.where(np.isnan(arr_wit_nans))
    for band_name in mb.band_names:
        mb[band_name] = arr_wit_nans
    mb = mb.fill_nans(-99)
    for band_name in mb.band_names:
        assert (mb[band_name][nan_locs] == -99).all()


def test_sb_from_path():
    dem_path = context.dem_paths[0]
    sb = pymagery.Raster.from_path(dem_path)
    assert type(sb) is pymagery.SingleBand
    assert sb.aff is not None
    assert sb.crs is not None


def test_mb_from_path():
    im_path = context.imagery_paths[0]
    mb = pymagery.Raster.from_path(im_path)
    assert type(mb) is pymagery.MultiBand
    assert mb.aff is not None
    assert mb.crs is not None


def test_rgb_from_path():
    im_path = context.imagery_paths[0]
    rgb = pymagery.RGB.from_path(im_path)
    assert type(rgb) is pymagery.RGB
    assert list(rgb.bands.keys()) == ['r', 'g', 'b', 'a']
