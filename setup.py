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
import platform
import sys

import setuptools
import setuptools.command.build_ext

OS = 'linux' if sys.platform.startswith('linux') else sys.platform
ARCH = platform.machine()
PLATFORM = '%s-%s' % (OS, ARCH)
HAS_PREBUILT = PLATFORM in ('linux-x86_64',)


class MyBuildExtCommand(setuptools.command.build_ext.build_ext):
    def run(self):
        setuptools.command.build_ext.build_ext.run(self)
        if HAS_PREBUILT:
            for ext in self.extensions:
                ext_path = self.get_ext_fullpath(ext.name)
                self.spawn([
                    'patchelf',
                    '--set-rpath',
                    '$ORIGIN/prebuilts/%s' % PLATFORM,
                    ext_path,
                ])


module1 = setuptools.Extension(
    'animeface._nvxs',
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
    ],
    library_dirs=[
        'animeface/prebuilts/%s' % PLATFORM,
    ])


setuptools.setup(
    name='animeface',
    version='1.1.0',
    author='takahashi.shuhei@gmail.com',
    author_email='takahashi.shuhei@gmail.com',
    url='https://github.com/nya3jp/python-animeface',
    description='A library to detect anime faces in images.',
    ext_modules=[module1],
    packages=['animeface'],
    package_data={'animeface': ['prebuilts/%s/libnvxs.so.0' % PLATFORM]},
    install_requires=['pillow'],
    cmdclass={
        'build_ext': MyBuildExtCommand,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
