#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

params = {
    'name':"remi",
    'description':"Python REMote Interface library",
    'use_scm_version':{'version_scheme': 'post-release'},
    'long_description':long_description,
    'long_description_content_type':"text/markdown",
    'url':"https://github.com/rawpython/remi",
    'download_url':"https://github.com/rawpython/remi/archive/master.zip",
    'keywords':["gui-library", "remi", "platform-independent", "ui", "gui"],
    'author':"Davide Rosa",
    'author_email':"dddomodossola@gmail.com",
    'license':"Apache",
    'packages':setuptools.find_packages(),
    'include_package_data':True,
    'setup_requires':['setuptools_scm'],
}
try:
    setup(**params)
except:
    del params['setup_requires']
    params['use_scm_version'] = False
    params['version'] = '2022.03.07'
    setup(**params)
