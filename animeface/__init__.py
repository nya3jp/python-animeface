# Copyright 2013 Shuhei Takahashi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from PIL.Image import Image

from animeface import _nvxs


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)


class Box:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def __repr__(self):
        return '(%d, %d; %d, %d)' % (self.x, self.y, self.width, self.height)


class Color:
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b

    def __repr__(self):
        return '(%d, %d, %d)' % (self.r, self.g, self.b)


class BoxColorPart:
    pos: Box
    color: Color

    def __init__(self, pos: Box, color: Color):
        self.pos = pos
        self.color = color

    def __repr__(self):
        return '<pos=%r, color=%r>' % (self.pos, self.color)


class PointPart:
    pos: Point

    def __init__(self, pos: Point):
        self.pos = pos

    def __repr__(self):
        return '<pos=%r>' % (self.pos, )


class BoxPart:
    pos: Box

    def __init__(self, pos: Box):
        self.pos = pos

    def __repr__(self):
        return '<pos=%r>' % (self.pos, )


class ColorPart:
    color: Color

    def __init__(self, color: Color):
        self.color = color

    def __repr__(self):
        return '<color=%r>' % (self.color, )


class Face:
    likelihood: float
    face: BoxPart
    skin: ColorPart
    hair: ColorPart
    left_eye: BoxColorPart
    right_eye: BoxColorPart
    mouth: BoxPart
    nose: PointPart
    chin: PointPart

    def __init__(self, result):
        self.likelihood = result['likelihood']
        self.face = BoxPart(Box(*result['face_box']))
        self.skin = ColorPart(Color(*result['skin_color']))
        self.hair = ColorPart(Color(*result['hair_color']))
        self.left_eye = BoxColorPart(Box(*result['left_eye_box']),
                                     Color(*result['left_eye_color']))
        self.right_eye = BoxColorPart(Box(*result['right_eye_box']),
                                      Color(*result['right_eye_color']))
        self.mouth = BoxPart(Box(*result['mouth_box']))
        self.nose = PointPart(Point(*result['nose_point']))
        self.chin = PointPart(Point(*result['chin_point']))

    def __repr__(self):
        return ('<animeface.Face '
                'likelihood=%(likelihood)f '
                'face=%(face)r '
                'skin=%(skin)r '
                'hair=%(hair)r '
                'left_eye=%(left_eye)r '
                'right_eye=%(right_eye)r '
                'mouth=%(mouth)r '
                'nose=%(nose)r '
                'chin=%(chin)r>') % self.__dict__


def detect(im: Image) -> List[Face]:
    """Detects anime faces.

  Args:
    im: PIL.Image object.

  Returns:
    A list of Face.
  """
    if im.mode in ('RGB', 'L'):
        pass  # Fine.
    elif im.mode == '1':
        im = im.convert('L')
    elif im.mode in ('P', 'RGBA', 'CMYK', 'YCbCr'):
        im = im.convert('RGB')
    else:
        raise ValueError('Unsupported color mode: %s' % im.mode)
    results = _nvxs.detect(im.getdata())
    return [Face(result) for result in results]
