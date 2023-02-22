#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/multicat

# packages with python3 setup.py -v sdist

from setuptools import setup, find_packages
from multicat.mc import __version__, desc

# Read project description
with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='multicat',
    version=__version__,
    author='r3nt0n',
    author_email='r3nt0n@protonmail.com',
    url='https://github.com/r3nt0n/multicat',
    license='GNU General Public License v3.0',
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        # If any package contains *.cfg files, include them
        '': ['*.cfg'],
    },
    #packages=['modules',],
    #packages=find_packages(),
    packages=['multicat'],
    #install_requires=[],
    entry_points = {
        'console_scripts':[
            'mc = multicat.mc:main'
        ]
    }
)