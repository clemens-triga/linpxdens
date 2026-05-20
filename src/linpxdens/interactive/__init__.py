"""
Image Linear Pixel Density Analyzer Interface

This module provides functionality for:
- Interactively selecting ROIs in images
- Fitting lines within selected ROIs
- Visualizing fitted lines and their properties
- Analyzing distances between multiple fitted lines

Dependencies:
    - cv2
    - numpy
    - matplotlib
    - line_collection (custom module)
    - distance_analyzer_core (custom module)
"""

from .session import analyze