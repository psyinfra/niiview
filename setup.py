#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='niiview',
      version='1',
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
	       ],
	  data_files = [
	       ('share/man', ['man/man1/niiview.1'])
	  ]
)
