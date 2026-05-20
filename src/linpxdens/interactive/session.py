"""
Interactive analysis module for line detection and ROI-based fitting.

This module provides an interactive workflow for selecting regions of interest
(ROIs) in an image, fitting linear structures within those regions, and
computing statistical properties of the detected line patterns.

Main functionality:
- Preprocessing of input images
- Interactive ROI selection and line fitting
- Collection of multiple validated line fits
- Full analysis pipeline with visualization

Workflow overview:
    1. Load image via core module
    2. Interactively select ROIs on the image
    3. Fit lines within selected ROIs
    4. Accept or reject fitted lines interactively
    5. Compute spacing statistics between accepted lines
    6. Visualize results (fit + distribution plots)
"""

import numpy as np

import core
from . import plotting as plot
from . import roi_selection as roi
from . import dialog as dia


def preprocess_image(image, roi_coords):
    """
    Preprocess the image by cropping to ROI and converting data type.

    :param image: Input image as NumPy array.
    :param roi_coords: Tuple (x, y, w, h) defining the ROI.
    :return: Cropped or original image as float32.
    """
    if np.issubdtype(image.dtype, np.unsignedinteger):
        image = image.astype(np.float32)
    if not roi_coords:
        return image
    else:
        x, y, w, h = roi_coords
        return image[y:y + h, x:x + w]


def collect_lines(image):
    """
    Interactive loop to collect multiple fitted lines from image.

    This function opens an interactive ROI selection interface where the user
    can repeatedly select regions of interest, fit lines, and decide whether
    to keep or discard each fitted result.

    :param image: Input image as NumPy array.
    :return: LineCollection containing all accepted fitted lines.
    """
    fig = None
    selector = None
    lines = core.LineCollection()

    while True:
        if fig is None or not plot.figure_exists(fig):
            fig, ax = roi.create_view(image)
            selector, event_dict = roi.attach_selector(ax)

        new_roi = roi.select(fig, selector, event_dict)
        if new_roi is False:
            plot.close_figure(fig)
            break

        fitted_line = core.fit_line(image, new_roi)
        line, point = plot.add_line(ax, fitted_line)

        if dia.confirm_fit(fig):
            lines.insert_line(fitted_line)
        else:
            plot.remove_line(line, point)

    return lines


def analyze(image_path):
    """
    Run full interactive image analysis pipeline.

    This function:
    - Loads an image from disk
    - Opens an interactive ROI-based line selection tool
    - Fits and collects multiple lines
    - Computes statistical spacing between lines
    - Generates visualization plots of results

    :param image_path: Path to input image file.
    :return: Tuple (mean, std, distances) representing line spacing statistics.
    :raises ValueError: If fewer than two valid lines are collected.
    """
    image = core.load_image(image_path)
    lines = collect_lines(image)

    if len(lines) < 2:
        raise ValueError("Not enough lines to calculate result")

    slope = lines.mean_slope
    centers = lines.centers

    fig_fit, ax_fit = plot.fit_results(image, centers, slope)

    mean, std, distances = core.get_mean_distance(lines)

    plot.distance_distribution(mean, std, distances)
    plot.show_figure()

    return mean, std, distances