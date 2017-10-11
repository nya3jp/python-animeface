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

from animeface import _nvxs


class Position(object):
  def __init__(self, pos_tuple):
    if isinstance(pos_tuple[0], tuple):
      self.x, self.y = pos_tuple[0]
      self.width, self.height = pos_tuple[1]
    else:
      self.x, self.y = pos_tuple

  def __repr__(self):
    if hasattr(self, 'width'):
      return '(%d, %d; %d, %d)' % (self.x, self.y, self.width, self.height)
    return '(%d, %d)' % (self.x, self.y)


class Color(object):
  def __init__(self, color_tuple):
    self.r, self.g, self.b = color_tuple

  def __repr__(self):
    return '(%d, %d, %d)' % (self.r, self.g, self.b)


class Part(object):
  def __init__(self, pos_tuple, color_tuple):
    if pos_tuple:
      self.pos = Position(pos_tuple)
    if color_tuple:
      self.color = Color(color_tuple)

  def __repr__(self):
    segs = []
    if hasattr(self, 'pos'):
      segs.append('pos=%r' % self.pos)
    if hasattr(self, 'color'):
      segs.append('color=%r' % self.color)
    return '<%s>' % ', '.join(segs)


class Face(object):
  def __init__(self, result):
    self.likelihood = result['likelihood']
    self.face = Part(result['face_pos'], None)
    self.skin = Part(None, result['skin_color'])
    self.hair = Part(None, result['hair_color'])
    self.left_eye = Part(result['left_eye_pos'], result['left_eye_color'])
    self.right_eye = Part(result['right_eye_pos'], result['right_eye_color'])
    self.mouth = Part(result['mouth_pos'], None)
    self.nose = Part(result['nose_pos'], None)
    self.chin = Part(result['chin_pos'], None)

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
            'chin=%(chin)r ') % self.__dict__


def detect(im):
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
