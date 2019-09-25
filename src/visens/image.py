import numpy as np
import matplotlib.pyplot as plt
from .load import load


def image(filename, colormap="viridis", vmin=None, vmax=None, log=False,
          side_panels=True, save=None, **kwargs):
    """
    Make a 2D image of the detector counts
    """

    data = load(filename, ids=True, **kwargs)

    z, edges = np.histogram(data.ids,
                            bins=np.arange(-0.5, data.nx * data.ny + 0.5))
    z = z.reshape(data.ny, data.nx)
    if side_panels:
        z_sumx = np.sum(z, axis=1)
        z_sumy = np.sum(z, axis=0)

    clab = "Counts"
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)
        clab = "log({})".format(clab)

    imstart = 0.1
    cbsize = 0.02
    if side_panels:
        imsize = 0.6
        ytitle = 1.38
    else:
        imsize = 0.75
        ytitle = 1.08
    plsize = 0.95 - imsize - 2.0 * imstart

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_axes([imstart, imstart, imsize, imsize])
    if side_panels:
        ax2 = fig.add_axes([1.0 - imstart, imstart, cbsize, imsize])
    else:
        ax2 = fig.add_axes([imstart + imsize + cbsize, imstart, cbsize, imsize])

    im = ax1.imshow(z, origin="lower", aspect="auto", interpolation="none",
                    vmin=vmin, vmax=vmax, extent=[data.x[0, 0], data.x[0, -1],
                                                  data.y[0, 0], data.y[-1, 0]])

    cb = plt.colorbar(im, ax=ax1, cax=ax2)
    if side_panels:
        cb.ax.set_xlabel(clab)
        cb.ax.xaxis.set_label_position("top")
    else:
        cb.ax.set_ylabel(clab)
    ax1.set_xlabel("x position [m]")
    ax1.set_ylabel("y position [m]")

    if side_panels:
        ax3 = fig.add_axes([imstart, imstart + imsize, imsize, plsize], sharex=ax1)
        ax4 = fig.add_axes([imstart + imsize, imstart, plsize, imsize], sharey=ax1)
        ax3.grid(True, color="lightgray", linestyle="dotted")
        ax4.grid(True, color="lightgray", linestyle="dotted")
        ax3.set_axisbelow(True)
        ax4.set_axisbelow(True)
        ax3.plot(data.x[0, :], z_sumy)
        ax4.plot(z_sumx, data.y[:, 0])
        ax3.set_xlim([data.x[0, 0], data.x[0, -1]])
        ax4.set_ylim([data.y[0, 0], data.y[-1, 0]])
        ax3.xaxis.tick_top()
        ax3.xaxis.set_label_position("top")
        ax4.yaxis.tick_right()
        ax3.set_xlabel("x position [m]")
        ax3.set_ylabel("Counts")
        ax4.set_xlabel("Counts")
        for tick in ax4.get_xticklabels():
            tick.set_rotation(-90)
        for tick in ax4.get_yticklabels():
            tick.set_rotation(-90)
        if side_panels == "log":
            ax3.set_yscale("log", nonposy="clip")
            ax4.set_xscale("log", nonposx="clip")
        ax3.set_title(filename.split("/")[-1], y=ytitle,
                      bbox=dict(facecolor="none", edgecolor="grey",
                                boxstyle="round"))
    else:
        ax1.set_title(filename.split("/")[-1], y=ytitle,
                      bbox=dict(facecolor="none", edgecolor="grey",
                                boxstyle="round"))

    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
