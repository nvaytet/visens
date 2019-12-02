import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from .imviewer import ImageViewer
from .load import load


def image(filename=None, data=None, colormap="viridis", vmin=None, vmax=None,
          log=False, side_panels=True, save=None, ax=None, **kwargs):
    """
    Make a 2D image of the detector counts
    """

    show = ax is None

    if data is None:
        data = load(filename, ids=True, **kwargs)

    z, edges = np.histogram(data.ids,
                            bins=np.arange(-0.5, data.nx * data.ny + 0.5))
    z = z.reshape(data.ny, data.nx)

    imv = ImageViewer(data.x[0, :], data.y[:, 0], z, filename=filename,
                      colormap=colormap, vmin=vmin, vmax=vmax, log=log,
                      side_panels=side_panels, clab="Counts", ax=ax,
                      xlabel="x position [m]", ylabel="y position [m]")

    if show:
        if save is not None:
            imv.fig.savefig(save, bbox_inches="tight")
        else:
            imv.fig.show()
