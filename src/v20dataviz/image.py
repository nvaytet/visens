import h5py
import numpy as np
import matplotlib.pyplot as plt


def image(filename,
          entry="/entry/instrument/detector_1/raw_event_data/event_id",
          colormap="viridis",
          vmin=None,
          vmax=None,
          log=False,
          nx=512,
          ny=512):
    """
    Make a 2D image of the detector counts
    """

    with h5py.File(filename, "r") as f:

        ids = np.array(f[entry][...], dtype=np.int32, copy=True)
        z, edges = np.histogram(ids, bins=np.arange(nx * ny + 1))
        z = z.reshape(nx, ny)
        if log:
            z = np.log10(z)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.imshow(z, origin="lower", aspect="equal", interpolation="none",
                       vmin=vmin, vmax=vmax)
        cb = plt.colorbar(im, ax=ax)
        cb.ax.set_ylabel("Counts")
        ax.set_xlabel("x position [m]")
        ax.set_ylabel("y position [m]")
        extension = "." + f.split(".")[-1]
        fig.savefig(f.replace(extension, ".pdf"), bbox_inches="tight")
