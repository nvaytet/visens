import numpy as np
import matplotlib.pyplot as plt
from .load import load


def tof(filename=None, data=None, xmin=None, xmax=None, logx=False, logy=False,
        logxy=False, nbins=512, save=None, ax=None, **kwargs):
    """
    Make counts vs tof histogram
    """

    if data is None:
        data = load(filename, tofs=True, **kwargs)

    tofs = data.tofs / 1.0e3
    if xmin is None:
        xmin = np.amin(tofs)
    if xmax is None:
        xmax = np.amax(tofs)

    show = True
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        show = False

    if logx or logxy:
        ax.set_xscale("log", nonposx='clip')
    if logy or logxy:
        ax.set_yscale("log", nonposy='clip')
    ax.hist(tofs, bins=np.linspace(xmin, xmax, nbins + 1))
    ax.set_xlabel("Time-of-flight [microseconds]")
    ax.set_ylabel("Counts")
    if filename is not None:
        ax.set_title(filename.split("/")[-1])

    if show:
        if save is not None:
            fig.savefig(save, bbox_inches="tight")
        else:
            plt.show()
