import numpy as np
import matplotlib.pyplot as plt
from .load import load
from .image import image
from .tof import tof
from .xy_vs_tof import x_vs_tof, y_vs_tof


def preview(filename=None, data=None, save=None, log=False, layout="2x2"):
    """
    Make a 4-panel file preview
    """

    if data is None:
        data = load(filename, ids=True, tofs=True, convert_ids=False)

    adjust = {"right": 0.85}

    ax = []
    swap = False
    if layout == "wide" or layout == "1x4":
        fig, ax = plt.subplots(1, 4, figsize=(20, 3))
        adjust["wspace"] = 0.83
        fact = 1.22
        titlepos = 1.18
    elif layout == "tall" or layout == "4x1":
        fig, ax = plt.subplots(4, 1, figsize=(3, 15))
        adjust["hspace"] = 0.5
        fact = 1.34
        titlepos = 1.04
    elif layout == "auto" or layout == "2x2":
        swap = True
        fig, ax = plt.subplots(2, 2, figsize=(9.5, 8))
        adjust["wspace"] = 0.78
        adjust["hspace"] = 0.5
        fact = 1.3
        titlepos = 1.01

    fig.subplots_adjust(**adjust)
    ax_list = ax.flatten()

    # Make the tof histogram wider than the rest
    pos = ax_list[0].get_position()
    points = pos.get_points()
    points[1][0] *= fact
    pos.set_points(points)
    ax_list[0].set_position(pos)

    # Limit the title length
    title_max_length = 40
    title = "{}".format(data.title)
    if len(title) > title_max_length:
        title = title[:title_max_length] + "..."
    tofs = data.tofs / 1.0e3
    header = (r"$\bf{" + filename.split("/")[-1].replace("_", "\\_") + "}$\n" +
              "Title: {}\nNumber of events: {}\n"
              "Min Tof: {} [microseconds]\n"
              "Max Tof: {} [microseconds]".format(
                title, len(tofs), np.min(tofs), np.max(tofs)))
    ax_list[0].text(-0.1, 1.05, header, ha="left", va="bottom", fontsize=10,
                    bbox=dict(facecolor="none", edgecolor="grey",
                              boxstyle="round"),
                    transform=ax_list[0].transAxes)

    tof(data=data, ax=ax_list[0], xmax=8.0e4)
    image(data=data, ax=ax_list[1 + swap], log=log, aspect="equal")
    x_vs_tof(data=data, ax=ax_list[2 - swap], log=log)
    y_vs_tof(data=data, ax=ax_list[3], log=log)

    if save is not None:
        fig.savefig(save, bbox_inches="tight", dpi=150)
    else:
        plt.show()
