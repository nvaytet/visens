import h5py
import numpy as np
import matplotlib.pyplot as plt


def image(filename,
          id_path="/entry/event_data/event_id",
          colormap="viridis",
          vmin=None,
          vmax=None,
          log=False,
          save=None):
    """
    Make a 2D image of the detector counts
    """

    with h5py.File(filename, "r") as f:

        ids = np.array(f[id_path][...], dtype=np.int32, copy=True)
        x = np.array(f["/entry/instrument/detector_1/x_pixel_offset"][...],
                     dtype=np.float64, copy=True)
        y = np.array(f["/entry/instrument/detector_1/y_pixel_offset"][...],
                     dtype=np.float64, copy=True)

    nx, ny = np.shape(x)
    z, edges = np.histogram(ids, bins=np.arange(nx * ny + 1))
    z = z.reshape(nx, ny)
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(z, origin="lower", aspect="equal", interpolation="none",
                   vmin=vmin, vmax=vmax,
                   extent=[x[0, 0], x[0, -1], y[0, 0], y[-1, 0]])
    cb = plt.colorbar(im, ax=ax)
    cb.ax.set_ylabel("Counts")
    ax.set_xlabel("x position [m]")
    ax.set_ylabel("y position [m]")
    ax.set_title(filename.split("/")[-1])
    if save is not None:
        extension = "." + f.split(".")[-1]
        fig.savefig(f.replace(extension, ".pdf"), bbox_inches="tight")
    else:
        plt.show()
