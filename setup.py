# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in kalachar/__init__.py
from kalachar import __version__ as version

setup(
	name='kalachar',
	version=version,
	description='To book dancers for culturals and workshops',
	author='av2l',
	author_email='kaviyaperiyasamy22@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
