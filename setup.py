#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="quo",
    install_requires=[
        "colorama; platform_system == 'Windows'",
        "pygments",
        "termcolor",
    ],
)
