"""Public package interface for crosszip."""

__all__ = ["__version__", "crosszip"]

from importlib.metadata import version

from .crosszip import crosszip

__version__ = version("crosszip")
