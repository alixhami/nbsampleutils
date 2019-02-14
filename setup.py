
# Copyright 2019 Alix Hamilton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbsampleutils",
    version="0.0.1",
    author="Alix Hamilton",
    author_email="alix.hamilton@gmail.com",
    description="Utilities for sample/tutorial notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alixhami/nbsampleutils",
    packages=setuptools.find_packages(),
    license="Apache Software License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
