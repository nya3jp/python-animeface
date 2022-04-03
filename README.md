# python-animeface

[![PyPI](https://img.shields.io/pypi/v/animeface.svg)](https://pypi.python.org/pypi/animeface)
[![Build](https://github.com/nya3jp/python-animeface/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/nya3jp/python-animeface/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/nya3jp/python-animeface.svg)](https://github.com/nya3jp/python-animeface/blob/main/LICENSE)

python-animeface is a Python wrapper of AnimeFace, a library to detect
anime character faces in images.

See also [the official website of AnimeFace](http://anime.udp.jp/imager-animeface.html)
(in Japanese language).


## Installation

### Installation with PIP via PyPI

You can install this module with PIP.

```
pip install animeface
```


### Manual installation

First, install libnvxs (the original AnimeFace library). It is included in this repository.

```
cd third_party/nvxs-1.0.2
./configure
make
sudo make install
```

Then install python-animeface.

```
python setup.py build
sudo python setup.py install
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

See [`animeface/__init__.py`](animeface/__init__.py) for the API definitions.


## License

python-animeface is licenced under [Apache License](LICENSE).

The original AnimeFace library is licenced under NYSL.
