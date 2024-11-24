#!/usr/bin/env python
from setuptools import setup

setup(
    entry_points={
        "pytest11": [
            "crosszip = crosszip.plugin",
        ],
    },
)
