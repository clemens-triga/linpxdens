"""
Core Linear Pixel Density Analyzer Module

Provides functionality to:
- Validate image paths and ROIs
- Load images
- Fit lines within specified ROIs
- Compute mean distance and statistics between fitted lines
- Perform high-level analysis combining these steps
"""

from .analysis import analyze, get_mean_distance, fit_line, load_image
from .line_collection import LineCollection