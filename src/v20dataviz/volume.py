import h5py
import numpy as np
import ipyvolume as ipv


def volume(filename,
           id_path="/entry/event_data/event_id",
           tof_path="/entry/event_data/event_time_offset",
           colormap="viridis",
           nbins=256):
    """
    Make a 3D volume rendering using ipyvolume
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
    z = np.transpose(z.reshape(nx, ny, nbins), axes=[2, 1, 0])
    ipv.quickvolshow(z,
        extent=[[x[0, 0]*100.0, x[0, -1]*100.0],
                [y[0, 0]*100.0, y[-1, 0]*100.0],
                [t[0], t[-1]]])
    ipv.pylab.xlabel("x [cm]")
    ipv.pylab.ylabel("y [cm]")
    ipv.pylab.zlabel("Tof [us]")
    ipv.show()

    return
