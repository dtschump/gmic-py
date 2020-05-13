import os

import pytest
import gmic
import numpy

from test_gmic_py import (
    gmic_instance_types,
    assert_gmic_images_are_identical,
    assert_non_empty_file_exists,
)

# Test parametrization: dtypes and interlacing toggling between two images
numpy_dtypes_base = (
    numpy.bool,
    numpy.longlong,
    numpy.single,
    numpy.double,
    numpy.longdouble,
    numpy.int8,
    numpy.int16,
    numpy.int32,
    numpy.uint8,
    numpy.uint16,
    numpy.uint32,
    numpy.float32,
    numpy.uint64,
    numpy.int64,
    numpy.float64,
    numpy.uint,
    numpy.intp,
    numpy.uintp,
)
nb_random_dtypes_to_test = 3
dtypes_testing_subset = [None] + list(
    numpy.random.choice(numpy_dtypes_base, nb_random_dtypes_to_test)
)
interleave_toggling_subset = (None, True, False)
numpy_dtypes1 = {"argnames": "dtype1", "argvalues": dtypes_testing_subset}
numpy_dtypes2 = {"argnames": "dtype2", "argvalues": dtypes_testing_subset}
interleave_toggles1 = {
    "argnames": "interleave1",
    "argvalues": interleave_toggling_subset,
}
interleave_toggles2 = {
    "argnames": "interleave2",
    "argvalues": interleave_toggling_subset,
}


@pytest.mark.parametrize(**gmic_instance_types)
def test_gmic_image_to_numpy_ndarray_exception_on_unimportable_numpy_module(
    gmic_instance_run,
):
    # numpy module hiding hack found at: https://stackoverflow.com/a/1350574/420684
    # Artificially prevent numpy from being imported
    import sys

    try:
        import numpy

        old_numpy_sys_value = sys.modules["numpy"]
    except:
        pass  # tolerate that numpy is already not importable
    else:
        # otherwise, make numpy not importable
        del numpy
        sys.modules["numpy"] = None

    import gmic

    images = []
    gmic.run(images=images, command="sp lena")
    with pytest.raises(gmic.GmicException, match=r".*'numpy' module cannot be imported.*"):
        images[0].to_numpy_array()

    # Repair our breaking of the numpy import
    sys.modules["numpy"] = old_numpy_sys_value


def gmic_image_to_numpy_array_default_interleave_param(i):
    return i if i is not None else True


def gmic_image_to_numpy_array_default_dtype_param(d):
    return d if d is not None else numpy.float32


@pytest.mark.parametrize(**numpy_dtypes1)
@pytest.mark.parametrize(**numpy_dtypes2)
@pytest.mark.parametrize(**interleave_toggles1)
@pytest.mark.parametrize(**interleave_toggles2)
@pytest.mark.parametrize(
    "gmic_command",
    ["""16,16,16,3 fill_color 255,222,30""", "sp apples"],
    ids=["2dsample", "3dsample"],
)
def test_gmic_image_to_numpy_array_fuzzying(
    dtype1, dtype2, interleave1, interleave2, gmic_command
):
    expected_interleave_check = gmic_image_to_numpy_array_default_interleave_param(
        interleave1
    ) == gmic_image_to_numpy_array_default_interleave_param(interleave2)
    params1 = {}
    params2 = {}
    if dtype1 is not None:
        params1["astype"] = dtype1
    if dtype2 is not None:
        params2["astype"] = dtype2
    if interleave1 is not None:
        params1["interleave"] = interleave1
    if interleave2 is not None:
        params2["interleave"] = interleave2

    single_image_list = []
    gmic.run(images=single_image_list, command=gmic_command)
    gmic_image = single_image_list[0]
    # Test default dtype parameter is numpy.float32
    numpy_image1 = gmic_image.to_numpy_array(**params1)
    numpy_image2 = gmic_image.to_numpy_array(**params2)
    assert numpy_image1.shape == numpy_image2.shape
    if gmic_image._depth > 1:  # 3d image shape checking
        assert numpy_image1.shape == (
            gmic_image._width,
            gmic_image._height,
            gmic_image._depth,
            gmic_image._spectrum,
        )
    else:  # 2d image shape checking
        assert numpy_image1.shape == (
            gmic_image._width,
            gmic_image._height,
            gmic_image._spectrum,
        )
    if dtype1 is None:
        dtype1 = numpy.float32
    if dtype2 is None:
        dtype2 = numpy.float32
    assert numpy_image1.dtype == dtype1
    assert numpy_image2.dtype == dtype2
    # Ensure arrays are equal only if we have same types and interlacing
    # Actually, they could be equal with distinct types but same interlacing, but are skipping cross-types compatibility analysis..
    if (numpy_image1.dtype == numpy_image2.dtype) and expected_interleave_check:
        assert numpy.array_equal(numpy_image1, numpy_image2)


@pytest.mark.parametrize(**gmic_instance_types)
def test_gmic_image_to_numpy_ndarray_basic_attributes(gmic_instance_run):
    import numpy

    single_image_list = []
    gmic_instance_run(images=single_image_list, command="sp apples")
    gmic_image = single_image_list[0]
    # we do not interleave to keep the same data structure for later comparison
    numpy_image = gmic_image.to_numpy_array(interleave=False)
    assert numpy_image.dtype == numpy.float32
    assert numpy_image.shape == (
        gmic_image._width,
        gmic_image._height,
        gmic_image._spectrum,
    )
    bb = numpy_image.tobytes()
    assert len(bb) == len(gmic_image._data)
    assert bb == gmic_image._data


@pytest.mark.parametrize(**gmic_instance_types)
def test_in_memory_gmic_image_to_numpy_nd_array_to_gmic_image(gmic_instance_run):
    single_image_list = []
    gmic_instance_run(images=single_image_list, command="sp lena")
    # TODO convert back and compare with original sp lena GmicImage


@pytest.mark.parametrize(**gmic_instance_types)
def test_numpy_ndarray_RGB_2D_image_gmic_run_without_gmicimage_wrapping(
    gmic_instance_run,
):
    # TODO completely uncoherent test now..
    import PIL.Image
    import numpy

    im1_name = "image.png"
    im2_name = "image.png"
    gmic_instance_run("sp lena output " + im1_name)
    np_PIL_image = numpy.array(PIL.Image.open(im1_name))
    # TODO line below must fail because single numpy arrays rewrite is impossible for us
    with pytest.raises(
        TypeError, match=r".*'images' parameter must be a 'gmic.GmicImage'.*"
    ):
        gmic_instance_run(images=np_PIL_image, command="output[0] " + im2_name)
    imgs = []
    gmic_instance_run(images=imgs, command="{} {}".format(im1_name, im2_name))
    assert_gmic_images_are_identical(imgs[0], imgs[1])

    # TODO input with list of numpy.ndarray's []
    # TODO input with list of mixed numpy and GmicImage objects[]


@pytest.mark.parametrize(**gmic_instance_types)
def test_numpy_ndarray_RGB_2D_image_integrity_through_numpyPIL_or_gmic_with_gmicimage_wrapping(
    gmic_instance_run,
):
    import PIL.Image
    import numpy

    im1_name = "image.bmp"
    im2_name = "image2.bmp"

    # 1. Generate lena bitmap, save it to disk
    gmic_instance_run("sp lena -output " + im1_name)

    # 2. Load disk lena through PIL/numpy, make it a GmicImage
    image_from_numpy = numpy.array(PIL.Image.open(im1_name))
    assert type(image_from_numpy) == numpy.ndarray
    assert image_from_numpy.shape == (512, 512, 3)
    assert image_from_numpy.dtype == "uint8"
    assert image_from_numpy.dtype.kind == "u"
    gmicimage_from_numpy = gmic.GmicImage(image_from_numpy)

    gmic_instance_run(images=gmicimage_from_numpy, command=("output[0] " + im2_name))

    # 3. Load lena into a regular GmicImage through G'MIC without PIL/numpy
    imgs = []
    gmic_instance_run(images=imgs, command="sp lena")
    gmicimage_from_gmic = imgs[0]

    # 4. Use G'MIC to compare both lena GmicImages from numpy and gmic sources
    assert_gmic_images_are_identical(gmicimage_from_numpy, gmicimage_from_gmic)
    assert_non_empty_file_exists(im1_name).unlink()
    assert_non_empty_file_exists(im2_name).unlink()


@pytest.mark.parametrize(**gmic_instance_types)
def test_numpy_PIL_modes_to_gmic(gmic_instance_run):
    import PIL.Image
    import numpy

    origin_image_name = "a.bmp"
    gmicimages = []
    gmic_instance_run("sp lena output " + origin_image_name)
    PILimage = PIL.Image.open("a.bmp")

    modes = [
        "1",
        "L",
        "P",
        "RGB",
        "RGBA",
        "CMYK",
        "YCbCr",
        "HSV",
        "I",
        "F",
    ]  # "LAB" skipped, cannot be converted from RGB

    for mode in modes:
        PILConvertedImage = PILimage.convert(mode=mode)
        NPArrayImages = [numpy.array(PILConvertedImage)]
        print(PILConvertedImage, NPArrayImages[0].shape, NPArrayImages[0].dtype)
        # gmic_instance_run(images=NPArrayImages, command="print") # TODO this segfaults.. more checking here

    # Outputs
    """
    <PIL.Image.Image image mode=1 size=512x512 at 0x7FAD99B18908> (512, 512) bool
    <PIL.Image.Image image mode=L size=512x512 at 0x7FAD324FD4E0> (512, 512) uint8
    <PIL.Image.Image image mode=P size=512x512 at 0x7FAD324FD8D0> (512, 512) uint8
    <PIL.Image.Image image mode=RGB size=512x512 at 0x7FAD324FD908> (512, 512, 3) uint8
    <PIL.Image.Image image mode=RGBA size=512x512 at 0x7FAD324FD8D0> (512, 512, 4) uint8
    <PIL.Image.Image image mode=CMYK size=512x512 at 0x7FAD324FD908> (512, 512, 4) uint8
    <PIL.Image.Image image mode=YCbCr size=512x512 at 0x7FAD324FD8D0> (512, 512, 3) uint8
    <PIL.Image.Image image mode=HSV size=512x512 at 0x7FAD324FD908> (512, 512, 3) uint8
    <PIL.Image.Image image mode=I size=512x512 at 0x7FAD324FD8D0> (512, 512) int32
    <PIL.Image.Image image mode=F size=512x512 at 0x7FAD324FD908> (512, 512) float32
    """

    assert_non_empty_file_exists(origin_image_name).unlink()


@pytest.mark.xfail(reason="method to implement soon")
def test_from_numpy_array_class_method_existence():
    # should not raise any AttributeError
    getattr(gmic.Gmic, "from_numpy_array")


# Useful for some IDEs with debugging support
if __name__ == "__main__":
    pytest.main([os.path.abspath(os.path.dirname(__file__))])