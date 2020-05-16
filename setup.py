#!/usr/bin/env python

from setuptools import setup, find_packages
from build_manpages import build_manpages, get_build_py_cmd, get_install_cmd
from setuptools.command.build_py import build_py
from setuptools.command.install import install

setup(name='niiview',
      version='2',
      description='A tool for displaying niftis in xterminals.',
      author='Tobias Kadelka',
      author_email='t.kadelka@fz-juelich.de',
      packages=find_packages(),
      license='LICENSE.txt',
      install_requires=[
    	'nibabel',
      'matplotlib',
      'numpy',
      'libsixel-python',
      'getkey',
      'Pillow'
      ],
	  scripts=[
	       'bin/niiview'
	       ]
	  cmdclass={
	        'build_manpages': build_manpages
	        }
)
