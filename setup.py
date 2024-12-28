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

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

module1 = setuptools.Extension('animeface._nvxs',
                               sources=[
                                   'animeface/_nvxs.c',
                               ],
                               include_dirs=[
                                   'third_party/Pillow-4.2.1/libImaging',
                                   'third_party/nvxs-1.0.2/nv_core',
                                   'third_party/nvxs-1.0.2/nv_ip',
                                   'third_party/nvxs-1.0.2/nv_ml',
                                   'third_party/nvxs-1.0.2/nv_face',
                                   'third_party/nvxs-1.0.2/nv_num',
                               ],
                               libraries=[
                                   'nvxs',
                               ])

setuptools.setup(
    name='animeface',
    author='takahashi.shuhei@gmail.com',
    author_email='takahashi.shuhei@gmail.com',
    url='https://github.com/nya3jp/python-animeface',
    description='A library to detect anime faces in images.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    use_scm_version={
        'root': '.',
        'relative_to': __file__,
        'local_scheme': 'node-and-date',
    },
    ext_modules=[module1],
    packages=['animeface'],
    setup_requires=['setuptools_scm'],
    install_requires=['pillow'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
