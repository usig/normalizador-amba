# coding: UTF-8
# !/usr/bin/env python
from __future__ import absolute_import
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import usig_normalizador_amba

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name=usig_normalizador_amba.__title__,
    version=usig_normalizador_amba.__version__,
    description=usig_normalizador_amba.__description__,
    long_description=readme,
    author=usig_normalizador_amba.__author__,
    author_email=usig_normalizador_amba.__author_email__,
    url='https://github.com/usig/normalizador-amba',
    license=usig_normalizador_amba.__license__,
    packages=['usig_normalizador_amba'],
    keywords='usig gcba gis normalizador direcciones amba',
    platforms=['Unix/Linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
