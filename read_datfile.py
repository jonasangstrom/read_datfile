import numpy as np
import struct


def read_dat(path):
    """ reads dat file in path and returns list of numpy arrays of
    frequencies, real part, imaginary part, the AC levels and the
    result number(?). The file contains more information, e.g.  timestamp(?)
    between 4 and 16
    """
    with open(path, 'rb') as binfile:
        content = binfile.read()

    data = content[66:-4]

    reals = []
    ims = []
    freqs = []
    AC_levels = []
    nbrs = []
    for n in range(len(data)//84):
        data_row = data[n*84: (n+1)*84]
        nbrs.append(bin_to_val(0, 4, 'xxh', data_row))
        AC_levels.append(bin_to_val(24, 32, 'd', data_row))
        freqs.append(bin_to_val(16, 24, 'd', data_row))
        reals.append(bin_to_val(64, 72, 'd', data_row))
        ims.append(bin_to_val(72, 80, 'd', data_row))
    results = [freqs, reals, ims, AC_levels, nbrs]

    return [np.array(result) for result in results]


def bin_to_val(start, stop, d_string, data_row):
    binary = data_row[start: stop]
    return struct.unpack(d_string, binary)
