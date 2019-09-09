import numpy as np
import matplotlib.pyplot as plt
from .load import load


def x_vs_tof(filename, colormap="viridis", vmin=None, vmax=None, log=False,
             nbins=512, save=None, transpose=False):
    """
    Make a x vs tof image
    """

    data = load(filename, ids=True, tofs=True)

    nx, ny = np.shape(data.x)
    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(nx * ny + 1), t])
    z = z.reshape(nx, ny, nbins)
    z = np.sum(z, axis=int(transpose==True))
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(z, origin="lower", aspect="auto", interpolation="none",
                   vmin=vmin, vmax=vmax,
                   extent=[t[0], t[-1], data.x[0, 0], data.x[0, -1]])
    cb = plt.colorbar(im, ax=ax)
    cb.ax.set_ylabel("Counts")
    ax.set_xlabel("Time-of-flight [microseconds]")
    ax.set_ylabel("x position [m]")
    ax.set_title(filename.split("/")[-1])
    if save is not None:
        extension = "." + f.split(".")[-1]
        fig.savefig(f.replace(extension, ".pdf"), bbox_inches="tight")
    else:
        plt.show()
