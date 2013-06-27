#!/usr/bin/python
#
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

import os
from setuptools import setup, Extension

module1 = Extension(
    'animeface._nvxs',
    sources=['animeface/_nvxs.c'],
    libraries=['nvxs'])

setup(
    name='animeface',
    version='1.0.2',
    author='takahashi.shuhei@gmail.com',
    author_email='takahashi.shuhei@gmail.com',
    url='https://github.com/nya3jp/python-animeface',
    description='A library to detect anime faces in images.',
    ext_modules=[module1],
    packages=['animeface'],
    install_requires=['PIL'],
    )
