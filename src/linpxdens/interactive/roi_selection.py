"""
ROI selection module for interactive image analysis.

This module provides tools for selecting rectangular regions of interest (ROIs)
on an image using an interactive matplotlib interface.
"""

import numpy as np
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt

from . import plotting as plot
from . import dialog as dia


def _collect_roi(event_container, eclick, erelease):
    """
    Rectangle selector callback to store ROI coordinates.

    :param event_container: Dictionary to store selection.
    :param eclick: Mouse press event.
    :param erelease: Mouse release event.
    """
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    event_container['roi'] = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def select(fig, selector, event_dict):
    """
    Wait for user to select ROI and confirm it.

    :param selector: RectangleSelector widget.
    :param event_dict: Dictionary storing selected ROI.
    :return: Tuple containing ROI coordinates or False if cancelled.
    """
    selector.set_active(True)
    selector.set_visible(True)
    fig.canvas.draw_idle()

    if 'roi' in event_dict:
        del event_dict['roi']

    while True:
        if dia.confirm_roi(fig):
            if 'roi' in event_dict:
                break
            else:
                print("No ROI found, try again.")
        else:
            return False

    selector.set_active(False)
    selector.set_visible(False)
    fig.canvas.draw_idle()

    return event_dict.get('roi')


def create_view(image):
    """
    Create a matplotlib figure for ROI selection.

    :param image: Input image as NumPy array.
    :return: Tuple (fig, ax) with displayed image.
    """
    fig, ax = plot.create_roi_view()
    ax.imshow(image, cmap='gray')
    return fig, ax


def attach_selector(ax):
    """
    Attach a RectangleSelector widget to a matplotlib axis.

    This enables interactive ROI selection via mouse dragging.

    :param ax: Matplotlib axis to attach selector to.
    :return: Tuple (selector, event_dict) where:
             - selector is the RectangleSelector instance
             - event_dict stores selected ROI coordinates
    """
    event_dict = {}
    selector = RectangleSelector(
        ax,
        lambda eclick, erelease: _collect_roi(event_dict, eclick, erelease),
        useblit=True,
        button=[1],
        minspanx=5,
        minspany=5,
        spancoords='pixels',
        interactive=True,
        ignore_event_outside=True,
        use_data_coordinates=True
    )
    return selector, event_dict