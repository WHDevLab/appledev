#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from setuptools import find_packages, setup

NAME = 'appstoreconnectapi'
DESCRIPTION = 'A Python wrapper around Apple AppStore Connect Api'
URL = 'https://github.com/whdevlab/appstoreconnectapi'
EMAIL = 'whdevlab@163.com'
AUTHOR = 'WHDevLab'
VERSION = None

REQUIRED = [
    'requests', 'PyJWT'
]

EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version='0.0.8',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT'
)
