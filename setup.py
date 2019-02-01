# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pycsvparse',
    version='0.1',
    description='Parse CSV and insert to sqllite',
    author='Paul Ryan',
    author_email='oriain@pm.me',
    url='https://github.com/daesu',
    packages=find_packages(exclude=('tests'))
)
