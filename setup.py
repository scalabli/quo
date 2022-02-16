#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="quo",
    install_requires=[
        "colorama; platform_system == 'Windows'",
        "pyperclip",
    #    "importlib-metadata; python_version < '3.8'", #InstallEd by default on Python3. 8 and later versions
    ],
)
