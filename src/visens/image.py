import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from .load import load


class ImageViewer():

    def __init__(self, x, y, z, filename=None, colormap="viridis", vmin=None,
                 vmax=None, log=False, side_panels=True, clab="", imstart=0.1,
                 ax=None):

        cbsize = 0.02
        figend = 0.95
        imsize = figend - 2.0 * imstart
        ytitle = 1.08
        if side_panels:
            plsize = 0.25 * imsize
            imsize = imsize - plsize
            ytitle = 1.38

        if vmin is None:
            vmin = np.nanmin(np.clip(z, 1.0, None) if log else z)
        if vmax is None:
            vmax = np.nanmax(np.clip(z, 1.0, None) if log else z)

        norm = LogNorm(vmin=vmin, vmax=vmax) if log else Normalize(vmin=vmin, vmax=vmax)

        self.side_panels = side_panels
        if ax is None:
            self.fig = plt.figure(figsize=(8, 8))
            self.ax1 = self.fig.add_axes([imstart, imstart, imsize, imsize])
            if self.side_panels:
                self.ax2 = self.fig.add_axes([1.0 - imstart, imstart, cbsize, imsize])
            else:
                self.ax2 = self.fig.add_axes([imstart + imsize + cbsize, imstart, cbsize, imsize])
        else:
            self.ax1 = ax
            self.ax2 = None

        self.im = self.ax1.imshow(z, origin="lower", aspect="auto", interpolation="none",
                                  norm=norm, extent=[x[0], x[-1], y[0], y[-1]])

        self.cb = plt.colorbar(self.im, ax=self.ax1, cax=self.ax2)
        if self.side_panels:
            self.cb.ax.set_xlabel(clab)
            self.cb.ax.xaxis.set_label_position("top")
        else:
            self.cb.ax.set_ylabel(clab)
        self.ax1.set_xlabel("x position [m]")
        self.ax1.set_ylabel("y position [m]")

        if self.side_panels:
            z_sumx = np.sum(z, axis=1)
            z_sumy = np.sum(z, axis=0)
            self.ax3 = self.fig.add_axes([imstart, imstart + imsize, imsize, plsize], sharex=self.ax1)
            self.ax4 = self.fig.add_axes([imstart + imsize, imstart, plsize, imsize], sharey=self.ax1)
            self.ax3.grid(True, color="lightgray", linestyle="dotted")
            self.ax4.grid(True, color="lightgray", linestyle="dotted")
            self.ax3.set_axisbelow(True)
            self.ax4.set_axisbelow(True)
            self.plot_x, = self.ax3.plot(x, z_sumy)
            self.plot_y, = self.ax4.plot(z_sumx, y)
            self.ax3.set_xlim([x[0], x[-1]])
            self.ax4.set_ylim([y[0], y[-1]])
            self.ax3.xaxis.tick_top()
            self.ax3.xaxis.set_label_position("top")
            self.ax4.yaxis.tick_right()
            self.ax3.set_xlabel("x position [m]")
            self.ax3.set_ylabel("Counts")
            self.ax4.set_xlabel("Counts")
            for tick in self.ax4.get_xticklabels():
                tick.set_rotation(-90)
            for tick in self.ax4.get_yticklabels():
                tick.set_rotation(-90)
            if log:
                self.ax3.set_yscale("log", nonposy="clip")
                self.ax4.set_xscale("log", nonposx="clip")
            self.ax3.set_title(filename.split("/")[-1], y=ytitle,
                               bbox=dict(facecolor="none", edgecolor="grey",
                                         boxstyle="round"))
        elif filename is not None:
            self.ax1.set_title(filename.split("/")[-1], y=ytitle,
                               bbox=dict(facecolor="none", edgecolor="grey",
                                         boxstyle="round"))
        return


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
                      side_panels=side_panels, clab="Counts", ax=ax)

    if show:
        if save is not None:
            imv.fig.savefig(save, bbox_inches="tight")
        else:
            imv.fig.show()
