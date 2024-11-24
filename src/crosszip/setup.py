from setuptools import setup, find_packages

setup(
    name="crosszip",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=6.0",
    ],
    entry_points={
        "pytest11": [
            "crosszip = crosszip.markers",
        ],
    },
    url="https://github.com/IndrajeetPatil/crosszip",
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
    ],
)
