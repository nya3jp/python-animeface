#!/bin/bash
# Copyright 2017 Shuhei Takahashi
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

set -ex

readonly -a versions=(cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39 cp310-cp310)

if [[ ! -d /host ]]; then
    echo "This must be run in a docker container"
    exit 1
fi

export HOME=/host/build/home
rm -rf "${HOME}"
mkdir -p "${HOME}"

# Build and install libnvxs.
(
    # CLAPACK tests need large stack size.
    ulimit -s 16384
    cd /host/third_party/nvxs-1.0.2
    ./configure --prefix="${HOME}"
    make
    make install
)

export LIBRARY_PATH="${HOME}/lib"
export LD_LIBRARY_PATH="${HOME}/lib"

for version in "${versions[@]}"; do
    "/opt/python/$version/bin/pip" wheel /host -w /tmp/wheels
done

for wheel in /tmp/wheels/animeface-*.whl; do
    auditwheel repair "$wheel" -w /tmp/wheels
    rm "$wheel"
done

for version in "${versions[@]}"; do
    "/opt/python/$version/bin/pip" install --no-index -f /tmp/wheels animeface
    "/opt/python/$version/bin/python" -c 'import animeface'
done

mkdir -p /host/wheels
cp /tmp/wheels/animeface-*.whl /host/wheels/
