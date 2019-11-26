import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from .load import load
from .image import ImageViewer

class Slicer(object):

    def __init__(self, x, y, z, tof, dt=0.0, filename="", colormap="viridis",
                 vmin=None, vmax=None, log=False, side_panels=True, clab=""):

        # Initial index
        self.ind = 0

        # Use ImageViewer class
        self.imv = ImageViewer(x, y, z[:, :, self.ind], filename=filename,
                      colormap=colormap, vmin=vmin, vmax=vmax, log=log,
                      side_panels=side_panels, clab=clab, imstart=0.12)

        self.x = x
        self.y = y
        self.z = z
        self.tof = tof
        self.dt = dt
        self.nslices = z.shape[-1]

        # Set limits
        if self.imv.side_panels:
            self.z_sumy = np.sum(z, axis=0)
            self.z_sumx = np.sum(z, axis=1)
            self.imv.ax3.set_ylim(top=np.nanmax(self.z_sumy))
            self.imv.ax4.set_xlim(right=np.nanmax(self.z_sumx))

        # Connect canvas to scroll
        self.imv.fig.canvas.mpl_connect("scroll_event", self.onscroll)

        # Add mpl slider widget
        self.ax_slider = self.imv.fig.add_axes([0.23, 0.02, 0.56, 0.03])
        self.slider = Slider(self.ax_slider, "Tof [us]", tof.min(), tof.max(),
                             valinit=tof.min())
        # Connect slider to function
        self.slider.on_changed(self.update)

    def onscroll(self, event):
        """
        Allow moving the slider with the mouse wheel
        """
        if event.button == "up":
            self.ind = np.clip(self.ind + 1, 0, self.nslices - 1)
        else:
            self.ind = np.clip(self.ind - 1, 0, self.nslices - 1)
        self.slider.set_val(self.ind * self.dt)

    def update(self, val=None):
        """
        Update the image with new data according to slider value
        """
        self.ind = np.clip(int(round(val/self.dt)), 0, self.nslices - 1)
        self.imv.im.set_data(self.z[:, :, self.ind])
        if self.imv.side_panels:
            self.imv.plot_x.set_data(self.x, self.z_sumy[:, self.ind])
            self.imv.plot_y.set_data(self.z_sumx[:, self.ind], self.y)


def slicer(filename=None, data=None, colormap="viridis", vmin=None, vmax=None,
           log=False, nbins=256, transpose=False, side_panels=True, **kwargs):
    """
    Make a 2D image viewer with a slider to navigate in the Tof dimension.
    You can also scroll with the mouse wheel to change the slider position.
    """

    if data is None:
        data = load(filename, ids=True, tofs=True, **kwargs)

    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(-0.5, data.nx * data.ny + 0.5),
                                     t])
    z = z.reshape(data.ny, data.nx, nbins)
    # Transpose should be True for old December 2018 files
    if transpose:
        z = np.transpose(z, axes=[1, 0, 2])

    # Create slicer object
    sl = Slicer(data.x[0, :], data.y[:, 0], z, 0.5*(t[1:] + t[:-1]),
                dt=t[1]-t[0], filename=filename, colormap=colormap, vmin=vmin,
                vmax=vmax, log=log, side_panels=side_panels, clab="Counts")
    # Assume we are always opening in interactive mode
    sl.imv.fig.show()

    return sl
