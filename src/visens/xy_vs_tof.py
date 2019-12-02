import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from .load import load
from .imviewer import ImageViewer


def xy_vs_tof(filename=None, data=None, colormap="viridis", vmin=None,
              vmax=None, log=False, nbins=512, save=None, axis="x",
              transpose=False, ax=None, side_panels=True, **kwargs):
    """
    Make a x or y vs tof image
    """

    show = ax is None

    if data is None:
        data = load(filename, ids=True, tofs=True, **kwargs)

    if axis == "x":
        sumaxis = int(transpose)
    elif axis == "y":
        sumaxis = int(not transpose)
    else:
        raise RuntimeError("Bad axis for x/y vs tof plot: {}".format(axis))

    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(-0.5, data.nx * data.ny + 0.5),
                                     t])
    z = z.reshape(data.ny, data.nx, nbins)
    z = np.sum(z, axis=sumaxis)

    if axis == "x":
        extent = [t[0], t[-1], data.x[0, 0], data.x[0, -1]]
        y = data.x[0, :]
    elif axis == "y":
        extent = [t[0], t[-1], data.y[0, 0], data.y[-1, 0]]
        y = data.y[:, 0]

    imv = ImageViewer(0.5 * (t[:-1] + t[1:]), y, z, filename=filename,
                      colormap=colormap, vmin=vmin, vmax=vmax, log=log,
                      side_panels=side_panels, clab="Counts", ax=ax,
                      xlabel="Time-of-flight [microseconds]",
                      ylabel="{} position [m]".format(axis),
                      extent=extent)

    if show:
        if save is not None:
            imv.fig.savefig(save, bbox_inches="tight")
        else:
            imv.fig.show()


def x_vs_tof(filename=None, data=None, colormap="viridis", vmin=None,
             vmax=None, log=False, nbins=512, save=None, transpose=False,
             ax=None, **kwargs):
    """
    Make a x vs tof image
    """

    xy_vs_tof(filename=filename, data=data, colormap=colormap, vmin=vmin,
              vmax=vmax, log=log, nbins=nbins, save=save, axis="x",
              transpose=transpose, ax=ax, **kwargs)


def y_vs_tof(filename=None, data=None, colormap="viridis", vmin=None,
             vmax=None, log=False, nbins=512, save=None, transpose=False,
             ax=None, **kwargs):
    """
    Make a y vs tof image
    """

    xy_vs_tof(filename=filename, data=data, colormap=colormap, vmin=vmin,
              vmax=vmax, log=log, nbins=nbins, save=save,
              axis="y", transpose=transpose, ax=ax, **kwargs)
