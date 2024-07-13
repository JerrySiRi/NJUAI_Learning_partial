#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Installs Match3-Cocos2d using distutils

Run:
    python setup.py install

to install this package.
"""
from setuptools import setup, find_packages
from os.path import join
from glob import glob

name = "match3cocos2d"

desc = "Match3 game using the Cocos2d Library"
long_desc = "Match3 game using the Cocos2d Library"


classifiers = '''
Development Status :: 1 - Planning
License :: Freely Distributable
License :: OSI Approved :: Apache2
Operating System :: OS Independent
Programming Language :: Python :: 2.7
'''

requirements = open('requirements.txt').read()

setup(
    name=name,
    version=open(join('match3cocos2d', 'version.txt')).readline().strip("\r\n"),
    description=desc,
    long_description=long_desc,
    author='João Pinto',
    author_email='lamego.pinto@gmail.com',
    classifiers=[x for x in classifiers.splitlines() if x],
    install_requires=[x for x in requirements.splitlines() if x],
    url='https://github.com/joaompinto/Match3-Cocos2d',
    packages=find_packages(),
    package_data={'images': ['*.png']},
    data_files=[(join('share', 'match3cocos2d', 'images'), glob(join('images', '*.png')))],
    include_package_data=True,
    entry_points={'console_scripts': ['match3-cocos2d = match3cocos2d.Main:main']}
)
