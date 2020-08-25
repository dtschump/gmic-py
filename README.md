<a href="https://gmic.eu">![G'MIC Logo](https://gmic.eu/img/logo4.jpg)</a>
<a href="https://www.python.org">![Python Logo](https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png)</a>

#### 
#### Python binding for G'MIC - A Full-Featured Open-Source Framework for Image Processing
##### https://gmic.eu

---------------------------

# gmic-py

![](https://github.com/myselfhimself/gmic-py/workflows/CPython%20GMIC%20Manylinux%202010%20%26%202014%20i686%20%26%20x86_64/badge.svg)
![](https://github.com/myselfhimself/gmic-py/workflows/CPython%20GMIC%20MacOS%20build/badge.svg)
![](https://github.com/dtschump/gmic-py/workflows/CPython%20GMIC%20Python%20package%20(Source%20and%20Debian/Ubuntu%20OS%20compilation)/badge.svg)

The aim of this project is to provide an official Python 3 package of the G'MIC image processing library, with its platform-specific binaries bundled or auto-compiled.
When this matures, running `pip install gmic-py` should be all you need to get ready and use G'MIC within data-science, games, video editing, texture editing etc.. Python scripts.

This project is a work in progress and lives under the CeCILL license (similar to GNU Public License).

## Documentation
Full documentation is being written at [https://gmic-py.readthedocs.io/](https://gmic-py.readthedocs.io/).

## Quickstart
You need Python 3.x and `pip` installed.
Things work best with the last development version for now :)

```bash
pip install gmic # Consider adding --only-binary if your machine makes you compile from source
python3
```
```python
import gmic
import struct
import random

random_32x32_image = gmic.GmicImage(struct.pack('1024f', *[random.randint(0, 255) for i in range(1024)]), 32, 32) 
random_32x32_image
# Output: <gmic.GmicImage object at 0x7f1084c41c90 with _data address at 0x2772010, w=32 h=32 d=1 s=1 shared=0>

gmic.run("print", images=random_32x32_image)
# Output:
# [gmic]-1./ Print image [0] = '[unnamed]'.
# [0] = '[unnamed]':
#   size = (32,32,1,1) [4096 b of floats].
#   data = (152,88,134,92,50,179,33,248,18,81,84,187,(...),54,42,179,121,125,74,67,171,224,240,174,96).
#   min = 0, max = 255, mean = 127.504, std = 75.1126, coords_min = (22,1,0,0), coords_max = (8,2,0,0).

# Reuse the same interpreter for better performance
reusable_gmic_instance = gmic.Gmic()
for a in range(10):
    reusable_gmic_instance.run("blur 2 print", images=random_32x32_image, image_names="my random blurred picture") # add "display" after "print" for a preview on Linux
# Output (first iteration only):
# [gmic]-1./ Print image [0] = 'my random blurred picture'.
# [0] = 'my random blurred picture':
#   size = (32,32,1,1) [4096 b of floats].
#   data = (146.317,134.651,125.137,117.714,115.019,118.531,121.125,123.81,121.736,120.603,123.06,130.212,(...),116.879,114.402,117.773,119.173,117.546,117.341,122.487,133.949,143.605,145.584,137.652,125.728).
#   min = 85.2638, max = 186.79, mean = 127.961, std = 11.9581, coords_min = (0,31,0,0), coords_max = (31,0,0,0).
```

## Official platform support
You can build your own Gmic python binding on possibly any platform with a C/C++ compiler.
Here is what we have managed to build and ship to [Gmic PyPI page](https://pypi.org/project/gmic/), allowing you to `pip install gmic` and use pre-built binaries or build `gmic-py` on the fly.
Note that `gmic-py`'s package installer links to your machine's existing `libpng`, `OpenMP` and `libcURL` if found.

| Build target                                                 | Basic gmic-py<sup>0</sup> |  ppm/bmp I/O    |  libpng I/O    | OpenMP | libcURL        | OpenCV         |
| -----------                                                  | ------------------------- | -----------     | ----------     |------- | -------        |--------        |
| Build from source<sup>1</sup>                                | ✓                         | ✓               | ✓ <sup>2</sup> | ✓      | ✓ <sup>2</sup> | ✓ <sup>2</sup> |
| Github CI Ubuntu Linux 64bit <sup>1</sup>                    | ✓                         | ✓               | ✓ <sup>2</sup> | ✓      | ✓ <sup>2</sup> | ✓ <sup>2</sup> |
| Pre-compiled Linux x86\_64 py3.6-3.9 (gcc)<sup>m</sup>| ✓                         | ✓               | ✓              | ✓      | ✓ <sup>3</sup> | ✗              |
| Pre-compiled MacOS 64 py3.6-3.9 (clang)                      | ✓                         | ✓               | ✓              | ✓      | ✓              | ✗              |
| Windows (planned)<sup>w</sup>                                | ✗                         | ✗               | ✗              | ✗      | ✗              | ✗              |

<sup>0</sup> ie. `gmic.GmicImage(bytes, w, h, d, s)`,  `gmic.run(..., "commands")`

<sup>1</sup> ie. from this project's tarball or using `pip install gmic` with the (possibly default) "from source" option. Hack the setup.py if needed, should work well with just `libz` installed, preferably with `libfftw3` too to support all sizes of images. Compiling with `gcc` or `clang` should work well.

<sup>2</sup> enabled if related library is found at compile time, using found `pkg-config` executable.

<sup>3</sup> useful for samples retrieval and getting the latest filters collection updated; libcurl is embedded in the wheel package. If failing, any runtime-findable `curl` executable will be used, see [this issue](https://github.com/myselfhimself/gmic-py/issues/9); at anytime, use the `network 0` G'MIC command to disable internet access

<sup>m</sup> those are actually manylinux2010 and manylinux2014 targets. Manylinux1 has been dropped

<sup>w</sup> Until it is ready, you can try building you own gmic-py builds on Windows using [MSYS2](https://www.msys2.org/)

## Examples

### Using your camera with G'MIC's optional OpenCV linking
If your machine has `libopencv` installed and your gmic-py was compiled from source (ie. `python setup.py build`), it will be dynamically linked.

[Example script](examples/opencv-camera/gmic-py-opencv-camera.py)

![Live example](examples/opencv-camera/gmic-py-opencv-camera.gif)

## Roadmap

### Q4 2019
1. Create a `pip install -e GITHUB_URL` installable Python package for GMIC, with an API very similar to the C++ library: `gmic_instance.run(...)`, `gmic(...)` and matching exception types. Binary dependencies [should be bundled as in this tutorial](https://python-packaging-tutorial.readthedocs.io/en/latest/binaries_dependencies.html).
    1. Through `Ctypes` dynamic binding on an Ubuntu docker image using Python 2-3. DONE in [ctypes\_archive branch](https://github.com/dtschump/gmic-py/tree/ctypes_archive).
    1. Through custom Python/C++ binding (see `gmicpy.cpp` and `setup.py`) DONE
1. Create documented examples for various application domains. WIP

### Q1-Q3 2020
1. Move the package to official Python package repositories. DONE
1. Add numpy nparray I/O support with automatic values (de-)interlacing WIP
1. Add Windows support

### Q2-Q3 2020
1. In a separate repository, create a Blender Plugin, leveraging the Python library and exposing: DONE
  1. a single Blender GMIC 2D node with a text field or linkable script to add a GMIC expression WIP
  1. as many 2D nodes as there are types of GMIC filters and commands (500+)
