# Build the dispersion relation based on the Fourier Transforms X and Y:
#
#   'histo' is a 2D array defined as np.zeros((f_binning, k_binning))
#
#   'dist' is the space distance between the two signals
#
#   'delta_f' and 'delta_k' are the spacing in f and k intervals
#
#   'f_binning' and 'k_binning' are the number of bins made in the f and k ranges
#   That is, 'delta' = range / 'binning'
#
#   The value of 'f_binning' is given by the total amount of samples in the signal
#   The value of 'k_binning' is arbitrary: not too small and not too big

def built_histo(histo, X, Y, dist, delta_f, delta_k, f_binning, k_binning):
    shift = (binning - 1)/2.
    # 'f_binning' frequencies and 'k_binning' wavenumbers
    Yc = np.conjugate(Y)
    k_f = np.angle(Yc*X) / dist   # Arrays of length 'f_binning' made of k(f)
    Power = np.abs(Yc*X)
    # print(k_f)

    # Relate the wavenumber k(f) to indexes in 'hist'
    indexes = np.zeros_like(k_f)
    indexes = np.floor(k_f / delta_k)
    # At the moment we have indexes spanning from -binning to +binning: shift them all!
    indexes += shift
    # print(k_f / delta_k)
    # print(indexes)
    indexes = indexes.astype(int)   # Cast 'indexes' into an array of integers

    js = np.arange(f_binning)   # Indexes of frequencies

    for index, j, p in zip(indexes, js, Power):
        histo[j, index] += p
        # print(p)
        # print(hist[j, index])

    return histo

# Some hints on how pcolormesh works: C must be an array of type np.array((Y, X))
# plt.pcolormesh([0,1,2,3], [0,1, 2], [[3, 2, 1, 0], [0, 0, 0, 0], [1, 1, 1, 1]], shading='nearest')
# plt.colorbar()
