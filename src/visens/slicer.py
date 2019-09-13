import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from .load import load


class Slicer(object):

    def __init__(self, fig, ax, X, tof, dt=0.0, vmin=None, vmax=None,
                 extent=None):
        self.fig = fig
        self.ax = ax
        self.ax.set_xlabel("x position [m]")
        self.ax.set_ylabel("y position [m]")

        self.X = X
        self.tof = tof
        self.dt = dt
        rows, cols, self.slices = X.shape
        self.ind = 0

        self.im = ax.imshow(self.X[:, :, self.ind], origin="lower",
                            aspect="equal", interpolation="none",
                            vmin=vmin, vmax=vmax, extent=extent)
        self.cb = plt.colorbar(self.im, ax=self.ax)
        self.cb.ax.set_ylabel("Counts")
        self.fig.canvas.mpl_connect("scroll_event", self.onscroll)

        # Add mpl slider widget
        self.ax_slider = self.fig.add_axes([0.23, 0.02, 0.56, 0.04])
        self.slider = Slider(self.ax_slider, "Tof [us]", tof.min(), tof.max(),
                             valinit=tof.min())
        # Connect slider to function
        self.slider.on_changed(self.update)

    def onscroll(self, event):
        """
        Allow moving the slider with the mouse wheel
        """
        if event.button == "up":
            self.ind = np.clip(self.ind + 1, 0, self.slices - 1)
        else:
            self.ind = np.clip(self.ind - 1, 0, self.slices - 1)
        self.slider.set_val(self.ind * self.dt)

    def update(self, val=None):
        """
        Update the image with new data according to slider value
        """
        self.ind = int(round(val/self.dt))
        self.im.set_data(self.X[:, :, self.ind])
        # self.ax.set_title("slice {}".format(self.ind))


def slicer(filename, colormap="viridis", vmin=None, vmax=None, log=False,
           nbins=256, transpose=False, **kwargs):
    """
    Make a 2D image viewer with a slider to navigate in the Tof dimension.
    You can also scroll with the mouse wheel to change the slider position.
    """

    data = load(filename, ids=True, tofs=True, **kwargs)

    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(-0.5, data.nx * data.ny + 0.5),
                                     t])
    z = z.reshape(data.nx, data.ny, nbins)
    # Transpose should be True for old December 2018 files
    if transpose:
        z = np.transpose(z, axes=[1, 0, 2])
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.log10(z)

    fig, ax = plt.subplots(1, 1)
    ax.set_title(filename.split("/")[-1])
    sl = Slicer(fig, ax, z, 0.5*(t[1:] + t[:-1]), dt=t[1]-t[0],
                vmin=vmin, vmax=vmax, extent=[data.x[0, 0], data.x[0, -1],
                                              data.y[0, 0], data.y[-1, 0]])
    plt.show()
    return sl
