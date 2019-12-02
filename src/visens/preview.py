import numpy as np
import matplotlib.pyplot as plt
from .load import load
from .image import image
from .tof import tof
from .xy_vs_tof import x_vs_tof, y_vs_tof


def preview(filename=None, data=None, save=None, log=False, wide=False):
    """
    Make a 4-panel file preview
    """

    if data is None:
        data = load(filename, ids=True, tofs=True, convert_ids=False)

    npanels = 4
    cbwidth = 0.01
    histwidth = 0.06
    histheight = 5 * histwidth
    gapx = 0.03
    paneldx = 0.2

    ax = []
    if wide:
        fig = plt.figure(figsize=(20, 4))
        # Tof
        ax.append(fig.add_axes([0.0, 0.0, paneldx, 1.0]))

        # xy image
        ax.append(fig.add_axes([paneldx + gapx, 0.0, paneldx, 1.0]))
        # xy cbar
        ax.append(fig.add_axes([2*paneldx + gapx + histwidth + 2*cbwidth, 0.0, cbwidth, 1.0]))
        # xy hist x
        ax.append(fig.add_axes([paneldx + gapx, 1.0, paneldx, histheight]))
        # xy hist y
        ax.append(fig.add_axes([2*paneldx + gapx, 0.0, histwidth, 1.0]))

        # xvstof image
        ax.append(fig.add_axes([2*paneldx + 3*gapx + 3*cbwidth + histwidth, 0.0, paneldx, 1.0]))
        # xvstof cbar
        ax.append(fig.add_axes([3*paneldx + 3*gapx + 5*cbwidth + 2*histwidth, 0.0, cbwidth, 1.0]))
        # xvstof hist x
        ax.append(fig.add_axes([2*paneldx + 3*gapx + 3*cbwidth + histwidth, 1.0, paneldx, histheight]))
        # xvstof hist y
        ax.append(fig.add_axes([3*paneldx + 3*gapx + 3*cbwidth + histwidth, 0.0, histwidth, 1.0]))

        # yvstof image
        ax.append(fig.add_axes([3*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 0.0, paneldx, 1.0]))
        # yvstof cbar
        ax.append(fig.add_axes([4*paneldx + 5*gapx + 8*cbwidth + 3*histwidth, 0.0, cbwidth, 1.0]))
        # yvstof hist x
        ax.append(fig.add_axes([3*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 1.0, paneldx, histheight]))
        # yvstof hist y
        ax.append(fig.add_axes([4*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 0.0, histwidth, 1.0]))
    else:
        fig = plt.figure(figsize=(12, 9))
        # Tof
        ax.append(fig.add_axes([0.0, 0.0, paneldx, 1.0]))

        # xy image
        ax.append(fig.add_axes([paneldx + gapx, 0.0, paneldx, 1.0]))
        # xy cbar
        ax.append(fig.add_axes([2*paneldx + gapx + histwidth + 2*cbwidth, 0.0, cbwidth, 1.0]))
        # xy hist x
        ax.append(fig.add_axes([paneldx + gapx, 1.0, paneldx, histheight]))
        # xy hist y
        ax.append(fig.add_axes([2*paneldx + gapx, 0.0, histwidth, 1.0]))

        # xvstof image
        ax.append(fig.add_axes([2*paneldx + 3*gapx + 3*cbwidth + histwidth, 0.0, paneldx, 1.0]))
        # xvstof cbar
        ax.append(fig.add_axes([3*paneldx + 3*gapx + 5*cbwidth + 2*histwidth, 0.0, cbwidth, 1.0]))
        # xvstof hist x
        ax.append(fig.add_axes([2*paneldx + 3*gapx + 3*cbwidth + histwidth, 1.0, paneldx, histheight]))
        # xvstof hist y
        ax.append(fig.add_axes([3*paneldx + 3*gapx + 3*cbwidth + histwidth, 0.0, histwidth, 1.0]))

        # yvstof image
        ax.append(fig.add_axes([3*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 0.0, paneldx, 1.0]))
        # yvstof cbar
        ax.append(fig.add_axes([4*paneldx + 5*gapx + 8*cbwidth + 3*histwidth, 0.0, cbwidth, 1.0]))
        # yvstof hist x
        ax.append(fig.add_axes([3*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 1.0, paneldx, histheight]))
        # yvstof hist y
        ax.append(fig.add_axes([4*paneldx + 5*gapx + 6*cbwidth + 2*histwidth, 0.0, histwidth, 1.0]))


    title_max_length = 40
    title = "{}".format(data.title)
    if len(title) > title_max_length:
        title = title[:title_max_length] + "..."
    tofs = data.tofs / 1.0e3
    print(filename.split("/")[-1].replace("_", "\\_"))
    header = (r"$\bf{" + filename.split("/")[-1].replace("_", "\\_") + "}$\n" +
        "Title: {}\nNumber of events: {}\n"
              "Min Tof: {} microseconds\n"
              "Max Tof: {} microseconds".format(title, len(tofs), np.min(tofs),
                                      np.max(tofs)))
    fig.text(0.0, 1.2, header, ha="left", va="center", fontsize=11,
             bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round"))

    tof(data=data, ax=ax[0])
    image(data=data, ax=ax[1:5], log=log, aspect="equal")
    x_vs_tof(data=data, ax=ax[5:9], log=log)
    y_vs_tof(data=data, ax=ax[9:13], log=log)

    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
