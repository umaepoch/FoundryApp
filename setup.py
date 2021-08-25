# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in foundryapp/__init__.py
from foundryapp import __version__ as version

setup(
	name='foundryapp',
	version=version,
	description='shipment container delivery',
	author='yashwanth',
	author_email='yashwanth@meritsystems.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
