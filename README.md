# python-animeface

[![Python versions](https://img.shields.io/pypi/pyversions/animeface)](https://pypi.org/project/animeface/)
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
[<animeface.Face likelihood=0.998505 face=<pos=(158, 126; 127, 127)> skin=<color=(252, 239, 232)> hair=<color=(89, 120, 165)> left_eye=<pos=(235, 148; 36, 32), color=(204, 68, 101)> right_eye=<pos=(235, 148; 36, 32), color=(141, 46, 67)> mouth=<pos=(224, 213; 18, 10)> nose=<pos=(222, 199)> chin=<pos=(236, 240)> ]
>>> fp = faces[0].face.pos
>>> print fp.x, fp.y, fp.width, fp.height
158 126 127 127
```

See [`animeface/__init__.py`](animeface/__init__.py) for the API definitions.


## License

python-animeface is licenced under [Apache License](LICENSE).

The original AnimeFace library is licenced under NYSL.
