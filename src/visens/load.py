import h5py
import numpy as np


class NxsData:
    """
    Class to hold data in Nexus file
    """

    def __init__(self, fields=None):

        for key in fields.keys():
            setattr(self, key, fields[key]["data"])

        return


def load(filename, ids=False, tofs=False, entry="/", verbose=False):
    """
    Load a hdf/nxs file and return required information.
    Note that the patterns are listed in order of preference,
    i.e. if more than one is present in the file, the data will be read
    from the first one found.
    """

    fields = {"x": {"pattern": ["/x_pixel_offset"],
                    "entry": None,
                    "data": None,
                    "dtype": np.float64},
              "y": {"pattern": ["/y_pixel_offset"],
                    "entry": None,
                    "data": None,
                    "dtype": np.float64}}

    if ids:
        fields["ids"] = {"pattern": ["/event_data/event_id",
                                     "/raw_event_data/event_id"],
                         "entry": None,
                         "data": None,
                         "dtype": np.int32}
    if tofs:
        fields["tofs"] = {"pattern": ["/event_data/event_time_offset",
                                      "/raw_event_data/event_time_offset"],
                          "entry": None,
                          "data": None,
                          "dtype": np.float64}

    with h5py.File(filename, "r") as f:

        contents = []
        f[entry].visit(contents.append)

        for item in contents:
            for key in fields.keys():
                if fields[key]["entry"] is None:
                    for p in fields[key]["pattern"]:
                        if item.endswith(p):
                            fields[key]["entry"] = item

        for key in fields.keys():
            fields[key]["data"] = np.array(f[fields[key]["entry"]][...],
                                           dtype=fields[key]["dtype"],
                                           copy=True)

    if verbose:
        for key in fields.keys():
            print("Loaded {} from: {}".format(key, fields[key]["entry"]))
            print("  - Data size: {} : Min={} , "
                  "Max={}".format(len(fields[key]["data"]),
                                  np.amin(fields[key]["data"]),
                                  np.amax(fields[key]["data"])))

    return NxsData(fields)
