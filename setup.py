# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in navdeepghai/__init__.py
from navdeepghai import __version__ as version

setup(
	name='navdeepghai',
	version=version,
	description='NavdeepGhai',
	author='NavdeepGhai',
	author_email='navdeepghai1@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
