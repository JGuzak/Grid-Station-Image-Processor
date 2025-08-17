"""
Grid Image Processor

A batch image processor for Monome Grid interface screenshots.
Crops to bracket intersections and resizes to standard dimensions.
"""

__version__ = "1.0.0"
__author__ = "Grid Image Processor"
__email__ = "example@example.com"

from .processor import GridImageProcessor

__all__ = ["GridImageProcessor"]
