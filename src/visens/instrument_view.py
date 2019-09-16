import h5py
import numpy as np
from matplotlib import cm


def instrument_view(filename,
           id_path="/entry/event_data/event_id",
           colormap="viridis",
           log=False,
           size=1):
    """
    Make a 3D instrument view using ipyvolume
    """

    try:
        import ipyvolume as ipv
    except ImportError:
        print("Instrument view makes use of the ipyvolume package which was "
              "not found on this system. Install using pip install ipyvolume.")


    with h5py.File(filename, "r") as f:

        ids = np.array(f[id_path][...], dtype=np.int32, copy=True)
        # tofs = np.array(f[tof_path][...], dtype=np.float64, copy=True) / 1.0e3
        x = np.array(f["/entry/instrument/detector_1/x_pixel_offset"][...],
                     dtype=np.float64, copy=True)
        y = np.array(f["/entry/instrument/detector_1/y_pixel_offset"][...],
                     dtype=np.float64, copy=True)


        # location = float(f["/entry/instrument/detector_1/transformations/location"][...])
        # loc_vec = np.array(f["/entry/instrument/detector_1/transformations/location"].attrs["vector"][...], dtype=np.float64, copy=True)
        # rotation = float(f["/entry/instrument/detector_1/transformations/orientation"][...])
        # rot_vec = np.array(f["/entry/instrument/detector_1/transformations/orientation"].attrs["vector"][...], dtype=np.float64, copy=True)

    nx, ny = np.shape(x)
    a, edges = np.histogram(ids, bins=np.arange(nx * ny + 1))
    a = a.reshape(nx, ny)
    if log:
        with np.errstate(divide="ignore", invalid="ignore"):
            a = np.log10(a)

    # x = x.flatten()
    # y = y.flatten()
    # a = a.flatten()

    z = np.zeros_like(x)

    # # Apply rotation
    # # TODO: this currently only works for rotation around y axis
    # # Need to generalise this with rotation matrix
    # rotation *= np.pi / 180.0
    # x = x * np.cos(rotation)
    # z = x * np.sin(rotation)
    # # Apply translation
    # x += location * loc_vec[0]
    # y += location * loc_vec[1]
    # z += location * loc_vec[2]

    # x *= 100.
    # y *= 100.
    # z *= 100.
    

    norm = cm.colors.Normalize(vmax=a.max(), vmin=a.min())
    colormap = cm.viridis
    color = colormap(norm(a.flatten()))

    # t = np.linspace(0.0, 7.2e4, nbins + 1)
    # z, xe, ye = np.histogram2d(ids, tofs, bins=[np.arange(nx * ny + 1), t])
    # z = np.transpose(z.reshape(nx, ny, nbins), axes=[2, 1, 0])
    # ipv.quickvolshow(z,
    #     extent=[[x[0, 0]*100.0, x[0, -1]*100.0],
    #             [y[0, 0]*100.0, y[-1, 0]*100.0],
    #             [t[0], t[-1]]])
    # ipv.pylab.xlabel("x [cm]")
    # ipv.pylab.ylabel("y [cm]")
    # ipv.pylab.zlabel("Tof [us]")
    # print(x)
    # print(y)
    # print(z)
    
    ipv.figure()
    x1, y1 = np.meshgrid([-1, 1], [-1, 1])
    w1 = ipv.plot_wireframe(x1, y1, np.ones_like(x1) * (-1.0), color="black")
    w2 = ipv.plot_wireframe(x1, y1, np.ones_like(x1), color="black")

    surf = ipv.plot_surface(x, y, z, color=color[...,:3])


    ipv.pylab.scatter([-1, -0.5], [-1, -0.5], [-1, -0.5], size=3, marker="sphere", color='r')
    ipv.show()

    return
