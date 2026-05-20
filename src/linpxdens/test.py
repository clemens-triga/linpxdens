import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

from interactive.session import analyze

def get_ax_by_label(fig, label):
    return next(
        (ax for ax in fig.axes if ax.get_label() == label),
        None
    )

def ask_confirmation(fig, question, true_label, false_label):
    result = {"value": None}
    fig.subplots_adjust(bottom=0.25)
    #button_ax = fig.add_axes([0.4, 0.05, 0.2, 0.08])
    #fig.suptitle(question, fontsize=14)

    def yes(event):
        result["value"] = True
        fig.canvas.stop_event_loop()

    def no(event):
        result["value"] = False

        fig.canvas.stop_event_loop()

    labels = [ax.get_label() for ax in fig.axes]

    if "btn_yes" in labels:
        ax_yes = get_ax_by_label(fig, "btn_yes")
        fig.delaxes(ax_yes)
    ax_yes  = fig.add_axes([0.2, 0.05, 0.25, 0.05])
    ax_yes.set_label("btn_yes")

    if "btn_no" in labels:
        ax_no = get_ax_by_label(fig, "btn_no")
        fig.delaxes(ax_no)
    ax_no   = fig.add_axes([0.55, 0.05, 0.25, 0.05])
    ax_no.set_label("btn_no")

    btn_yes = Button(ax_yes, true_label)
    btn_no  = Button(ax_no, false_label)

    btn_yes.on_clicked(yes)
    btn_no.on_clicked(no)

    fig.text(
        0.5, 0.16,
        question,
        ha="center",
        va="center",
        fontsize=12
    )
   #plt.show(block=False)

    # wait until user clicks
    #while result["value"] is None:
    #    plt.pause(1)

    fig.show()
    fig.canvas.start_event_loop(timeout=-1)    
    

    return result["value"]

def confirm_roi(fig):
    question = "Please select ROI with selector?"
    true_label = "Done"
    false_label = "Exit"
    return ask_confirmation(fig,question, true_label, false_label)

def confirm_fit(fig):
    question ="Is the acquired fit good?"
    true_label = "Yes"
    false_label = "No"
    return ask_confirmation(fig,question, true_label, false_label)


#img = np.random.rand(100, 100)

#fig, ax = plt.subplots(figsize=(5, 5))
#ax.imshow(img, cmap="gray")
#ax.set_title("Image")
#print(confirm_roi(fig))
#print(confirm_fit(fig))
#print(fig.axes)
#for i, ax in enumerate(fig.axes):
#    print(i, ax.get_title())
analyze("/home/clemens/TU-Wien/Dokumente/Unterlagen_TRIGA/Radiographie/Software/Python_Scripts/Optical_resolution/image_20250326_083803.tif")