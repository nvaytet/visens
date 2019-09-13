import numpy as np
import matplotlib.pyplot as plt
from .load import load


def image(filename, colormap="viridis", vmin=None, vmax=None, log=False,
          save=None, **kwargs):
    """
    Make a 2D image of the detector counts
    """

    data = load(filename, ids=True, **kwargs)

    z, edges = np.histogram(data.ids,
                            bins=np.arange(-0.5, data.nx * data.ny + 0.5))
    z = z.reshape(data.nx, data.ny)
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(z, origin="lower", aspect="equal", interpolation="none",
                   vmin=vmin, vmax=vmax, extent=[data.x[0, 0], data.x[0, -1],
                                                 data.y[0, 0], data.y[-1, 0]])
    cb = plt.colorbar(im, ax=ax)
    cb.ax.set_ylabel("Counts")
    ax.set_xlabel("x position [m]")
    ax.set_ylabel("y position [m]")
    ax.set_title(filename.split("/")[-1])
    if save is not None:
        fig.savefig(save, bbox_inches="tight")
    else:
        plt.show()
