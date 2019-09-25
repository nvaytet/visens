import numpy as np
import matplotlib.pyplot as plt
from .load import load


def x_vs_tof(filename, colormap="viridis", vmin=None, vmax=None, log=False,
             nbins=512, save=None, transpose=False, **kwargs):
    """
    Make a x vs tof image
    """

    data = load(filename, ids=True, tofs=True, **kwargs)

    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(-0.5, data.nx * data.ny + 0.5),
                                     t])
    z = z.reshape(data.ny, data.nx, nbins)
    z = np.sum(z, axis=int(transpose))
    clab = "Counts"
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)
        clab = "log({})".format(clab)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(z, origin="lower", aspect="auto", interpolation="none",
                   vmin=vmin, vmax=vmax,
                   extent=[t[0], t[-1], data.x[0, 0], data.x[0, -1]])
    cb = plt.colorbar(im, ax=ax)
    cb.ax.set_ylabel(clab)
    ax.set_xlabel("Time-of-flight [microseconds]")
    ax.set_ylabel("x position [m]")
    ax.set_title(filename.split("/")[-1])
    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
