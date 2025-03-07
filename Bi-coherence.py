#%% BI-COHERENCE <---------- DONE

# You can either use the pybispectra package or the hand made function:
#
#   NOTE: the data format taken by 'pybispectra' is pretty strange
#         It is a 3D array where axis 0 relate to epochs, axis 1 to channels and axis to the sample.
#         That is, data[1, 2, 3] indicate the 3rd value in channel 2 of the 1st epoch.
#         
#         Epoch = segment in which you divide the entire signal
#         Channel = practically speaking, the channels of an oscilloscope (different chnl = different signal)
#         Sample = the sampled values
#
#         See the following example stored in pybispectra for more:
#    
#         temp = np.load(get_example_data_paths("sim_data_pac_bivariate"))
#
#
#   The hand written function compute the bi-coherence for only one time series.
#   Specifically, it divides the signal 'x' in segments of 'win_len' length and
#   proceeds in computing the Short Time Fourier Transform of each segment.
#
#   Followingly, the STFTs should be sliced in order to reduce the computational cost by
#   a factor 'f_hop', if I manage (IN THE FUTURE) to implement it.
#   Clearly, a large 'f_hop' would decrease the computation time and the storage size of 'B'.
#
#   Then, it evaluates the bi-spectrum and the normalization factors,
#   in doing so it starts from the low frequencies.
#   
#
#   Finally, the function 'plot_bicoherence' plots using an even more sliced version
#   of the bi-coherence, in order to reduce further the computational cost in plotting.
#
#
#   Furthermore, I also compute the summed bi-coherence with the 'summed_bicoherence' function.




#---------- Making of bi-coherence diagram with a hand written function

# 'win_len': Size of each sample (default: 4999)
# The algorithm works for an even value of f_pts, which is given by 'win_len' + 1
# Thus 'win_len' MUST BE AN ODD NUMBER.
#
# 'win_hop': Size of the hop between samples (default: 2500),
#            thus the overalp is given by 'win_len' - 'win_hop'.
#            For better averaging, a high overlap is suggested.

# NOTE: 'plt.pcolormesh' plots a 2D array starting from the lower left corner and goes row by row
# Thus 'B' will be made of f_pts rows (corresponding to y = 0, ..., f_Nyquist) of length f_pts each

def compute_bicoherence (x, fs = 1e6, win_len = 9999, win_hop = 1000, f_hop = 1):
    
    # Controlling sequences:
    #   NOTE: if you set win_len, win_hop, f_hop = 9999, 1000, 1 it works fine!
    #   Which makes sense, because is almost the parameters used for the spectrograms!
    
    if (f_hop%2 == 1 and f_hop != 1):
        print('\a')
        print("\n\nf_hop should be even!\n\n")
        return 0, 0, 0
    elif (win_len%2 == 0):
        print('\a')
        print("\n\nwin_len MUST be ODD!\n\n")
        return 0, 0, 0
    
    # my_win = windows.tukey(win_len, alpha = 0.25)   # Suggested in scipy.spectrogram()
    # my_win = windows.parzen(win_len)
    my_win = windows.blackman(win_len)

    SFT = ShortTimeFFT(win = my_win, hop = win_hop, fs = fs)
    
    # 'Fts' is structured as: np.array((number_of_frequencies, number_of_STFTs))
    # That is, FTs[0][6] indicates the 1st frequence in the 7th SFTF
    
    FTs = SFT.stft(x)
    f_pts = SFT.f_pts   # Number of frequencies
    n_seg = len(FTs[0])   # Number of segments = Number of STFTs = Number of columns in 'FTs'
    
    # '''
    # # In order to reduce the computational cost while keeping the high accuracy of the STFT,
    # # I re-sample the obtained STFTs by slicing them with the hop term 'f_hop'.
    # # 
    # # Remember that a[::4] leads to [a_0, a_4, a_8, a_12, ..., a_4k],
    # # given for example a = [a_0, a_1, a_2, ..., a_4k, a_4k+1, a_4k+2, a_N].
    # # Where N = 4k + r, with r = 1, 2 or 3. Thus, it throws away what is beyond a_4k.
    
    # if (f_hop != 1):
    #     FTs = FTs[::f_hop, :]
    #     f_pts = (f_pts // f_hop) + 1
    # '''
        
    half_pts = int(f_pts/2)   # Because I compute only the lower half of bi-spectrum
    
    B = np.zeros((half_pts, f_pts), dtype=complex)   # Bi-spectrum
    N_1 = np.zeros((half_pts, f_pts), dtype=float)   # Normalization factors for bi-coherence
    N_2 = np.zeros((half_pts, f_pts), dtype=float)   # Normalization factors for bi-coherence
    
    for i in range(0, half_pts):   # For every row i, starting from the lower left corner
    
        print(f"In i = {i}/{half_pts - 1}", end = '\r')
        
        for j in range(0, n_seg):
            
            # This row has 'f_pts' elements and the first frequency corresponds to 0 Hz!
            if (i == 0):
                B[i,:] += FTs[i, j]*FTs[:, j]*np.conjugate(FTs[:, j])
                N_1[i, :] += np.abs(FTs[i, j]*FTs[:, j])**2
                N_2[i, :] += np.abs(FTs[:, j])**2
            else: 
                k = FTs[i, j]   # STFT of frequency i
                m = FTs[:, j]   # STFT of every frequency
                n = np.concatenate((np.zeros(i), np.conjugate(FTs[2*i:, j]), np.zeros(i)))                
                B[i, :] += k*m*n   # i-th frequency * all frequencies * sum of them
                N_1[i, :] += np.abs(k*m)**2
                N_2[i, :] += np.abs(n)**2
            
    # Evaluate the averages
    B = B / n_seg
    N_1 = N_1 / n_seg
    N_2 = N_2 / n_seg
    
    # Remove the 0s from the normalization factors
    N_1[np.abs(N_1) < 1e-10] = 1.
    N_2[np.abs(N_2) < 1e-10] = 1.
    
    # Compute the bi-coherence
    b = np.abs(B)**2 / (N_1*N_2)
    
    return B, b, SFT.f[::f_hop]
    
# For the computation of the summed bi-coherence, I proceed as follows:
#   - given that b has an even number of rows and columns, we evaluate 2 freqs at a time
#   - watch the following scheme, where the number inside patches is the index of f = f_x + f_y:
#
#   f_y
#       |-----|-----|-----|-----|-----|-----|-----|-----|
#   f_3 |     |     |     | f_6 | f_7 |     |     |     |
#       |-----|-----|-----|-----|-----|-----|-----|-----|
#   f_2 |     |     | f_4 | f_5 | f_6 | f_7 |     |     |
#       |-----|-----|-----|-----|-----|-----|-----|-----|
#   f_1 |     | f_2 | f_3 | f_4 | f_5 | f_6 | f_7 |     |
#       |-----|-----|-----|-----|-----|-----|-----|-----|
#   f_0 | f_0 | f_1 | f_2 | f_3 | f_4 | f_5 | f_6 | f_7 |
#       |-----|-----|-----|-----|-----|-----|-----|-----|
#         f_0   f_1   f_2   f_3   f_4   f_5   f_6   f_7    f_x
#
#   - couple 0: 
#                f_0 from col 0 of row 0
#                f_1 from col 1 of row 0
#   - couple 1: 
#                f_2 from col 2 of row 0, col 1 of row 1
#                f_3 from col 3 of row 0, col 2 of row 1
#   - couple 2: 
#                f_4 from col 4 of row 0, col 3 of row 1, col 2 of row 2
#                f_5 from col 5 of row 0, col 4 of row 1, col 3 of row 2
#   - couple 3: 
#                f_6 from col 6 of row 0, col 5 of row 1, col 4 of row 2, col 3 of row 3
#                f_7 from col 7 of row 0, col 6 of row 1, col 5 of row 2, col 4 of row 3
#
#   - thus 'i' indicates the couple index, and 'j' the current row; therefore
#     'j' goes from 0 to 'i' included, while 'i' goes from 0 to total number of rows.

def summed_bicoherence(b):
    n_rows = len(b[:, 0])
    n_cols = len(b[0])   # Total number of frequencies
    
    sb = np.zeros(n_cols)
    
    for i in range(0, n_rows):
        N = 0
        print(f"i={i}")
        
        for j in range(0, i+1):
            sb[2*i] += b[j, 2*i-j]
            sb[2*i + 1] += b[j, 2*i + 1 - j]
            N += 1
            
        sb[2*i] = sb[2*i]/N
        sb[2*i + 1] = sb[2*i + 1]/N
    
    return sb

def plot_bicoherence(b, f, win_len = 4999):
    
    hops = int((win_len + 1)/1000)
    
    f_pts = int(win_len + 1)/2
    
    xf_range = f[::hops]*10**(-3)
    yf_range = f[0:int(f_pts/2):hops]*10**(-3)
    z = b[::hops, ::hops]
    
    # MAKE PLOT WITH 'plt.contourf'
    
    X, Y = np.meshgrid(xf_range, yf_range)

    #   X and Y contains the bounds of each patch, while z is the value *inside* each patch.
    #   Therefore, length of z is one less than that of X and Y.
    z = z[:-1, :-1]   # <--- It removes the highest frequencies of the bi-spectrum

    #   Choose how much levels (i.e. colors) the colormap has for drawing.
    #   Let's say there are 20 + 1 colors between the min and max of the bi-spectrum
    levels = mpl.ticker.MaxNLocator(nbins=20).tick_values(z.min(), z.max())

    #    Pick the desired colormap
    cmap = plt.colormaps['plasma']

    fig, ax1 = plt.subplots(1, 1)
    dx = (xf_range[1] - xf_range[0])
    dy = (yf_range[1] - yf_range[0])
    cf = ax1.contourf(X[:-1, :-1] + dx/2., Y[:-1, :-1] + dy/2., z, 
                      levels = levels, cmap = cmap)
    fig.colorbar(cf, ax = ax1).set_label('$b^2 (\omega_1, \omega_2)$', fontsize=16)
    ax1.set_title('Bi-coherence')
    ax1.set_xlabel(r'$f_1$ [kHz]')
    ax1.set_ylabel(r'$f_2$ [kHz]')
    
    # MAKE PLOT WITH 'plt.pcolormesh'
    
    # plt.pcolormesh(xf_range, yf_range, z, shading='nearest')
    # plt.colorbar().set_label('$|B|$', fontsize=13)
    # plt.ylabel(r'[kHz]', fontsize=13)
    # plt.xlabel(r'[kHz]', fontsize=13)
    # plt.title('Bi-coherence', fontsize=13)


#---------- Making of bi-coherence diagram with pybispectra

# '''
# def compute_B2 (x, fs = 1e6, win_len = 5000, win_hop = 2500):
    
#     # my_win = windows.tukey(win_len, alpha = 0.25)   # Use the one suggested in scipy.spectrogram()
#     my_win = windows.parzen(win_len)

#     SFT = ShortTimeFFT(win = my_win, hop = win_hop, fs = fs)
    
#     # 'Fts' is structured as: np.array((number_of_frequencies, number_of_STFTs))
#     # That is, FTs[0][6] indicates the 1st frequence in the 7th SFTF
    
#     FTs = SFT.stft(x)
#     freqs = SFT.f
#     sampling_freq = fs
# '''
