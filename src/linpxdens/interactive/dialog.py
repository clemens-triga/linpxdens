"""
Interactive dialog utilities for user-driven image analysis workflow.

This module provides simple GUI-based confirmation dialogs using matplotlib
widgets. It is used to control interactive steps in the analysis pipeline,
such as ROI confirmation and validation of fitted results.
"""

import sys
from matplotlib.widgets import Button
from . import plotting as plot
from . import dialog as dia


def ask_confirmation(fig, question, true_label, false_label):
    """
    Display a confirmation dialog inside a matplotlib figure.

    The dialog adds two buttons to the figure and blocks execution until
    the user selects one of the available options or closes the figure.

    :param fig: Figure used to display the confirmation dialog.
    :type fig: matplotlib.figure.Figure
    :param question: Question displayed to the user.
    :type question: str
    :param true_label: Label of the confirmation button.
    :type true_label: str
    :param false_label: Label of the rejection button.
    :type false_label: str
    :return: True if the confirmation button was pressed,
             False otherwise.
    :rtype: bool
    """
    result = {"value": None}

    fig.subplots_adjust(bottom=0.25)

    def on_confirm(event):
        """
        Handle confirmation button click.

        :param event: Matplotlib button click event.
        """
        result["value"] = True
        fig.canvas.stop_event_loop()

    def on_reject(event):
        """
        Handle rejection button click.

        :param event: Matplotlib button click or close event.
        """
        result["value"] = False
        fig.canvas.stop_event_loop()

    def on_close(event):
        """
        Handle figure close event.

        :param event: Matplotlib button click or close event.
        """
        plot.close_figure(fig)
        sys.exit(0)

    fig.canvas.mpl_connect("close_event", on_close)

    txt_question = fig.text(
        0.5, 0.16,
        question,
        ha="center",
        va="center",
        fontsize=12
    )

    ax_yes = fig.add_axes([0.2, 0.05, 0.25, 0.05])
    ax_no = fig.add_axes([0.55, 0.05, 0.25, 0.05])

    btn_yes = Button(ax_yes, true_label)
    btn_no = Button(ax_no, false_label)

    cid_yes = btn_yes.on_clicked(on_confirm)
    cid_no = btn_no.on_clicked(on_reject)

    close_cid = fig.canvas.mpl_connect("close_event", on_close)

    #plot.show_figure(fig, block=False)
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(timeout=-1)

    #while result["value"] is None:
    #    plot.wait(0.05)

    # disconnect callbacks first
    fig.canvas.mpl_disconnect(close_cid)
    btn_yes.disconnect(cid_yes)
    btn_no.disconnect(cid_no)

    # remove artists/widgets
    ax_yes.remove()
    ax_no.remove()
    txt_question.remove()

    # redraw
    #fig.canvas.draw_idle()

    return result["value"]


def confirm_roi(fig):
    """
    Ask the user to confirm the selected ROI.

    This dialog is typically used after interactive ROI selection
    to allow the user to continue or abort the workflow.

    :param fig: Figure containing the ROI visualization.
    :type fig: matplotlib.figure.Figure
    :return: True if the ROI selection is confirmed, otherwise False.
    :rtype: bool
    """
    question = "Please select ROI with selector?"
    true_label = "Done"
    false_label = "End"
    return ask_confirmation(fig, question, true_label, false_label)


def confirm_fit(fig):
    """
    Ask the user to confirm whether a fitted result is acceptable.

    This dialog is typically displayed after a line fitting step
    during interactive analysis.

    :param fig: Figure displaying the fitted result.
    :type fig: matplotlib.figure.Figure
    :return: True if the fit is accepted, otherwise False.
    :rtype: bool
    """
    question = "Is the acquired fit good?"
    true_label = "Yes"
    false_label = "No"
    return ask_confirmation(fig, question, true_label, false_label)