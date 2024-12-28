# python-animeface

[![PyPI](https://img.shields.io/pypi/v/animeface.svg)](https://pypi.python.org/pypi/animeface)
[![Build](https://github.com/nya3jp/python-animeface/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/nya3jp/python-animeface/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/nya3jp/python-animeface.svg)](https://github.com/nya3jp/python-animeface/blob/main/LICENSE)

python-animeface is a Python wrapper of AnimeFace, a library to detect
anime character faces in images.

See also [the official website of AnimeFace] (in Japanese language).

[the official website of AnimeFace]: http://anime.udp.jp/imager-animeface.html


## Installation

You can install this module with PIP.

```
pip install animeface
```

In case a Python binary package (wheel) is not available for your environment,
you need to install libnvxs (the original AnimeFace library) before installing
python-animeface. The source code of libnvxs is included in this repository.

```
cd third_party/nvxs-1.0.2
./configure
make
sudo make install
```


## Usage

```
>>> import animeface
>>> import PIL.Image
>>> im = PIL.Image.open('/path/to/image.jpg')
>>> faces = animeface.detect(im)
>>> faces
[<animeface.Face likelihood=1.000000 face=<pos=(295, 90; 182, 182)> skin=<color=(253, 226, 212)> hair=<color=(199, 194, 196)> left_eye=<pos=(408, 134; 34, 42), color=(92, 42, 49)> right_eye=<pos=(316, 137; 55, 48), color=(79, 33, 39)> mouth=<pos=(372, 202; 32, 23)> nose=<pos=(397, 186)> chin=<pos=(377, 242)>>]
>>> fp = faces[0].face.pos
>>> print(fp.x, fp.y, fp.width, fp.height)
295 90 182 182
```

See [`animeface/__init__.py`] for the API definitions.

[`animeface/__init__.py`]: https://github.com/nya3jp/python-animeface/blob/main/animeface/__init__.py


## Changelog

### 2.0.3 (2024-12-28)

- Fix libnvxs build on modern Mac.
- Add prebuilts for Python 3.13.
- Add prebuilts for ARM Mac.
- Drop prebuilts for Intel Mac.

### 2.0.2 (2023-12-28)

- No functional changes.
- Add prebuilts for Python 3.11-3.12.
- Drop prebuilts for Python 3.6-3.7.

### 2.0.0 (2022-04-04)

- The first modern release.
- Include prebuilt libnvxs in wheels.
- Support Python 3.6+.
- Add type annotations.

## License

python-animeface is licenced under [Apache License](LICENSE).

The original AnimeFace library is licenced under NYSL.
