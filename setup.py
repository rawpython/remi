#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="remi",
    description="Python REMote Interface library",
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dddomodossola/remi",
    download_url="https://github.com/dddomodossola/remi/archive/master.zip",
    keywords=["gui-library", "remi", "platform-independent", "ui", "gui"],
    author="Davide Rosa",
    author_email="dddomodossola@gmail.com",
    license="Apache",
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
)
