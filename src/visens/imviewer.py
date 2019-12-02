import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize


class ImageViewer():

    def __init__(self, x, y, z, filename=None, colormap="viridis", vmin=None,
                 vmax=None, log=False, side_panels=True, clab="", imstart=0.1,
                 ax=None, aspect="auto", xlabel=None, ylabel=None,
                 extent=None):

        histsize = 0.25

        if vmin is None:
            vmin = np.nanmin(np.clip(z, 1.0, None) if log else z)
        if vmax is None:
            vmax = np.nanmax(np.clip(z, 1.0, None) if log else z)

        norm = LogNorm(vmin=vmin, vmax=vmax) if log else Normalize(vmin=vmin, vmax=vmax)

        self.side_panels = side_panels
        if ax is None:
            self.fig, self.ax1 = plt.subplots(1, 1, figsize=(7, 7))
            if self.side_panels:
                self.fig.subplots_adjust(bottom=0.15, top=0.76, right=0.74)
            else:
                self.fig.subplots_adjust(bottom=0.15, top=0.90, right=0.87)
        else:
            self.ax1 = ax
        if self.side_panels:
            self.ax2 = self.ax1.inset_axes([1.3, 0.0, 0.04, 1.0])
            ytitle = 1.08
        else:
            self.ax2 = self.ax1.inset_axes([1.03, 0.0, 0.04, 1.0])
            ytitle = 1.03

        if extent is None:
            extent = [x[0], x[-1], y[0], y[-1]]

        self.im = self.ax1.imshow(z, origin="lower", aspect=aspect, interpolation="none",
                                  norm=norm, extent=extent)

        self.cb = plt.colorbar(self.im, ax=self.ax1, cax=self.ax2)
        if self.side_panels:
            self.cb.ax.set_xlabel(clab)
            self.cb.ax.xaxis.set_label_position("top")
        else:
            self.cb.ax.set_ylabel(clab)
        self.ax1.set_xlabel(xlabel)
        self.ax1.set_ylabel(ylabel)

        if self.side_panels:
            z_sumx = np.sum(z, axis=1)
            z_sumy = np.sum(z, axis=0)
            self.ax3 = self.ax1.inset_axes([0.0, 1.0, 1.0, histsize], sharex=self.ax1)
            self.ax4 = self.ax1.inset_axes([1.0, 0.0, histsize, 1.0], sharey=self.ax1)
            self.ax3.grid(True, color="lightgray", linestyle="dotted")
            self.ax4.grid(True, color="lightgray", linestyle="dotted")
            self.ax3.set_axisbelow(True)
            self.ax4.set_axisbelow(True)
            self.plot_x, = self.ax3.plot(x, z_sumy)
            self.plot_y, = self.ax4.plot(z_sumx, y)
            self.ax3.set_xlim([extent[0], extent[1]])
            self.ax4.set_ylim([extent[2], extent[3]])
            self.ax3.xaxis.tick_top()
            self.ax4.yaxis.tick_right()
            self.ax3.set_ylabel("Counts")
            self.ax4.set_xlabel("Counts")
            for tick in self.ax3.get_xticklabels():
                tick.set_visible(False)
            for tick in self.ax4.get_yticklabels():
                tick.set_visible(False)
            if log:
                self.ax3.set_yscale("log", nonposy="clip")
                self.ax4.set_xscale("log", nonposx="clip")
            if filename is not None:
                self.ax3.set_title(filename.split("/")[-1], y=ytitle,
                                   bbox=dict(facecolor="none", edgecolor="grey",
                                             boxstyle="round"))
        elif filename is not None:
            self.ax1.set_title(filename.split("/")[-1], y=ytitle,
                               bbox=dict(facecolor="none", edgecolor="grey",
                                         boxstyle="round"))
        return
