import h5py
import numpy as np
import matplotlib.pyplot as plt


def x_vs_tof(filename,
          id_path="/entry/event_data/event_id",
          tof_path="/entry/event_data/event_time_offset",
          colormap="viridis",
          vmin=None,
          vmax=None,
          log=False,
          nbins=512,
          save=None,
          transpose=False):
    """
    Make a x vs tof image
    """

    with h5py.File(filename, "r") as f:

        ids = np.array(f[id_path][...], dtype=np.int32, copy=True)
        tofs = np.array(f[tof_path][...], dtype=np.float64, copy=True) / 1.0e3
        x = np.array(f["/entry/instrument/detector_1/x_pixel_offset"][...],
                     dtype=np.float64, copy=True)
        y = np.array(f["/entry/instrument/detector_1/y_pixel_offset"][...],
                     dtype=np.float64, copy=True)
        nx, ny = np.shape(x)
        t = np.linspace(0.0, 7.2e4, nbins + 1)
        z, xe, ye = np.histogram2d(ids, tofs, bins=[np.arange(nx * ny + 1), t])
        z = z.reshape(nx, ny, nbins)
        z = np.sum(z, axis=int(transpose==True))
        if log:
            z = np.log10(z)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.imshow(z, origin="lower", aspect="auto", interpolation="none",
                       vmin=vmin, vmax=vmax,
                       extent=[t[0], t[-1], x[0, 0], x[0, -1]])
        cb = plt.colorbar(im, ax=ax)
        cb.ax.set_ylabel("Counts")
        ax.set_xlabel("Time-of-flight [microseconds]")
        ax.set_ylabel("x position [m]")
        if save is not None:
            extension = "." + f.split(".")[-1]
            fig.savefig(f.replace(extension, ".pdf"), bbox_inches="tight")
        else:
            plt.show()
