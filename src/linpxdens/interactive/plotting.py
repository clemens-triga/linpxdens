"""
Plotting utilities for interactive image analysis and line fitting visualization.

This module provides helper functions for visualizing image-based line fitting
results, ROI selection, and statistical distance analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


def create_roi_view():
    """
    Create a figure and axes for interactive ROI selection.

    The figure is initialized with a predefined title and window name
    for selecting a region of interest (ROI) from an image.

    :return: Tuple containing the created matplotlib figure and axes.
    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
    """
    fig, ax = plt.subplots()
    fig.suptitle("Select ROI from the Image", fontsize=16)
    fig.canvas.manager.set_window_title("Selection")
    return fig, ax


def figure_exists(fig):
    """
    Check whether a matplotlib figure still exists.

    :param fig: Figure object to check.
    :type fig: matplotlib.figure.Figure
    :return: True if the figure exists, otherwise False.
    :rtype: bool
    """
    return plt.fignum_exists(fig.number)


def show_figure(figure=None, **kwargs):
    """
    Display a matplotlib figure.

    If a figure is provided, it is activated before showing.

    :param figure: Optional matplotlib figure to display.
    :type figure: matplotlib.figure.Figure | None
    :param kwargs: Additional keyword arguments passed to plt.show()
    """
    if figure is not None:
        plt.figure(figure.number)

    plt.show(**kwargs)


def close_figure(fig):
    """
    Close a matplotlib figure.

    :param fig: Figure to close.
    :type fig: matplotlib.figure.Figure
    """
    plt.close(fig)

def wait(time):
    plt.pause(time)
    


def add_line(ax, line_data):
    """
    Add a fitted line and its center point to an axes object.

    The function plots a line based on slope and intercept values and
    marks the corresponding center point. A legend is updated with
    the line parameters.

    :param ax: Matplotlib axes object where the line is drawn.
    :type ax: matplotlib.axes.Axes
    :param line_data: Tuple containing slope, intercept, and center point
                      coordinates in the format
                      ``(slope, intercept, (center_x, center_y))``.
    :type line_data: tuple[float, float, tuple[float, float]]
    :return: Handles to the created line and point objects.
    :rtype: tuple[matplotlib.lines.Line2D, matplotlib.lines.Line2D]
    """
    slope, intercept, (center_x, center_y) = line_data
    x_min, x_max = ax.get_xlim()
    x_img = np.array([x_min, x_max])
    y_img = slope * x_img + intercept

    line, = ax.plot(x_img, y_img, color="green", linewidth=0.5)
    point, = ax.plot(center_x, center_y, marker='o', color='red', linestyle='None')

    labels = [f"Slope = {slope:.2f}", f"Center = ({center_x:.2f}, {center_y:.2f})"]
    ax.legend([line, point], labels, ncol=1)

    plt.pause(0.1)
    return line, point


def remove_line(line, point):
    """
    Remove a plotted line and point from the figure.

    :param line: Line object to remove.
    :type line: matplotlib.lines.Line2D
    :param point: Point object to remove.
    :type point: matplotlib.lines.Line2D
    """
    line.remove()
    point.remove()
    plt.pause(0.1)


def fit_results(image, centers, slope):
    """
    Plot fitted lines on top of an image.

    A line is drawn through each provided center point using the
    specified average slope.

    :param image: Input image displayed in grayscale.
    :type image: numpy.ndarray
    :param centers: List of center points in ``(x, y)`` format.
    :type centers: list[tuple[float, float]]
    :param slope: Average slope used for all fitted lines.
    :type slope: float
    :return: Tuple containing the created figure and axes.
    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
    """
    fig, ax = plt.subplots()
    fig.suptitle("Line Fit Results", fontsize=16)
    fig.canvas.manager.set_window_title("Line Fits")

    ax.imshow(image, cmap='gray')

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    x = np.array([x_min, x_max])

    line_handle = None
    for i, center in enumerate(centers):
        y_fit = slope * (x - center[0]) + center[1]
        line, = ax.plot(x, y_fit, color='red', linewidth=0.5)
        if i == 0:
            line_handle = line

    if line_handle:
        ax.legend([line_handle], [f"Slope: {slope:.2f}"])

    plt.xlim(left=x_min, right=x_max)
    plt.ylim(bottom=y_min, top=y_max)

    return fig, ax


def distance_distribution(mean, std, distances):
    """
    Plot the distribution of distances between fitted lines.

    The histogram includes markers for the mean distance and the
    standard deviation range.

    :param mean: Mean value of the distances.
    :type mean: float
    :param std: Standard deviation of the distances.
    :type std: float
    :param distances: Sequence of measured distances.
    :type distances: list[float] | numpy.ndarray
    :return: Tuple containing the created figure and axes.
    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
    """
    fig, ax = plt.subplots()
    fig.suptitle("Distance Distribution", fontsize=16)
    fig.canvas.manager.set_window_title("Result")

    ax.hist(distances, bins=30, edgecolor='black')
    ax.axvline(x=mean, color='orange', label=f"Mean = {mean:.2f}")
    ax.axvline(x=mean + (std / 2), color='green', linestyle='--', label=f"Std = {std:.2f}")
    ax.axvline(x=mean - (std / 2), color='green', linestyle='--')

    ax.legend()
    return fig, ax