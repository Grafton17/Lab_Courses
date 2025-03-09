def conditional_sampling(ref, meas, low_bound = -np.inf, high_bound = np.inf,
                         use_std = True, tau_shifts = np.array([0])):
    
    # tau_shift is an array of all time shifts to be considered
    
    if (use_std==True):
        mean = np.mean(ref)
        std = np.std(ref, ddof=1, mean=mean)   # ddof=1 uses Bessel's correction
        
        low_bound = low_bound*std + mean
        high_bound = high_bound*std + mean
    
    #----- Use boolean indexing, which seems to be faster than np.where()
    
    all_cond_means = np.array([])   # Will contain all time shifts for a fixed point in space
    
    for tau in tau_shifts:
        
        cond_ref2 = ref.copy()
        cond_meas2 = meas.copy()
        
        if (tau > 0):
            cond_ref2 = cond_ref2[:-tau]
            cond_meas2 = cond_meas2[tau:] 
        elif (tau < 0):
            cond_ref2 = cond_ref2[-tau:]   # Note that -tau is > 0!
            cond_meas2 = cond_meas2[:tau]
        
        cond_meas2[cond_ref2 < low_bound] = 0
        cond_meas2[cond_ref2 > high_bound] = 0
    
    #----- Instead of boolean indexing, one can use the np.where() routine,
    #      which is a little bit slower than the used method. To see the latter,
    #      check the 'speed_checks.py' script.
    
    # cond_meas = np.where(low_bound < ref, np.where(ref < high_bound, meas, 0), 0)
    # cond_ref  = np.where(low_bound < ref, np.where(ref < high_bound, ref,  0), 0)
    
    # print(f"{np.array_equal(cond_meas, cond_meas2)}")   # <--- They are indeed equal!
    
    #----- Some visual confirmations
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # j = 0000
    
    # ax1.plot(time[j:j+10000], ref[j:j+10000], label='Original')
    # ax1.plot(time[j:j+10000], cond_ref2[j:j+10000], label='Filtered')
    # ax1.legend()
    # ax1.grid()
    # ax1.axhline(low_bound, color='k')
    # ax1.axhline(high_bound, color='k')
    
    # ax2.plot(time[j:j+10000], meas[j:j+10000], label='Original')
    # ax2.plot(time[j:j+10000], cond_meas2[j:j+10000], label='Filtered')
    # ax2.legend()
    # ax2.grid()
    
    #----- Evaluate the conditional mean
    
        N = np.count_nonzero(cond_meas2)
        cond_mean = np.sum(cond_meas2)/N
        
        all_cond_means = np.append(all_cond_means, cond_mean)
        
    return all_cond_means   # Returns simultaneously all the time shifted C.A.s

#---------- SAVE THE POLOIDAL VISUALISATIONS

# The following function plot the poloidal distribution of the C.A. values.
#
# To do so, we can use the 'plt.colormesh' routine, which is easy to use but
# has a limited set of usable interpolations between grid points; or, we can
# use the 'plt.imshow' routine which draws the 2D distribution independetly of
# X and Y grid underneath it. So it's up to the user to set the correct extents
# of the axes: use the 'extent' parameter which, for origin = 'lower' accepts as
# input (x_low, x_high, y_low, y_hig).
#
# NOTE: the axes extent for 1.5 grid units on both vertical and horizontal sides!
#
# The C.A.s are not passed as a 2D array, but as a 1D instead. They are gridded 
# via the 'scipy.interpolate.griddata' routine.

def saveplot_conditional_sampling(tau_shift, set_name):

    # Loading of the data, thus 'path' is just a string of my file tree.
    # The 'pos' array stores the coordinates of each grid point inside the Thorello machine.
    filepath = set_name + '/' + str(tau_shift)
    pos = np.loadtxt(path + '/Programmi/Analisi condizionale/giusti10_DA_USARE.txt')
    means = np.loadtxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt')
    
    xpos = pos[:, 3]
    ypos = pos[:, 4]
    xside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70]
    yside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
    X, Y = np.meshgrid(xside, yside)

    # z = means[:, 1]
    z = means

    # Available interpolations: nearest, linear or cubic
    grid_z0 = griddata((xpos, ypos), z, (X, Y), method='linear')

    #----- MAKE PLOT WITH 'plt.imshow'
    # If you wanna know a linear color scale, remove the 'norm' parameter and put
    # instead vmin = -50. and vmax = +3. parameters.
    #
    # Available interesting norms are SymLogNorm and PowerNorm, see the
    # proper documentation on matplotlib's site for more.
    
    plt.imshow(grid_z0, interpolation = 'hamming', origin = 'lower',
              extent = (-85, 75, -85, 85),
              aspect = 'auto', cmap = 'Spectral', 
              norm=colors.PowerNorm(vmin = -50., vmax = +3., gamma=3))
    
    plt.plot(xpos, ypos, 'ok', alpha=0.5, markersize=2)
    plt.plot(0, 0, 'X', color='white', markersize=10)
    plt.colorbar().set_label('$V_F$', fontsize=16)
    plt.xlabel('R [cm]')
    plt.ylabel('Z [cm]')
    plt.title(rf'$<V_M>_C$ at $\tau$ = {tau_shift:.2f} [$\mu$s]')
    plt.minorticks_on()
    plt.grid()

    filepath = set_name + '/Immagini/' + str(100000+tau_shift) + '_' + str(tau_shift)
    plt.savefig(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.png')
    plt.savefig(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.pdf')
    
    plt.close()
    
    #----- MAKE PLOT WITH 'plt.pcolormesh' ---> impossibility to use cool interpolations :(
        
    # plt.pcolormesh(X, Y, grid_z0, shading='nearest', cmap='Spectral')
    # plt.colorbar().set_label('$V_F$', fontsize=13)
    # plt.ylabel('Z [cm]')
    # plt.xlabel('R [cm]')
    # plt.title(r'$\tau$ = 0')

#---------- UPDATE FRAMES IN THE ANIMATION CREATION

# This function is identical to the last one just seen, but the 'tau_shift'
# parameter is instead linked to frame number 'frame'.
# 'frame' is a number passed by the 'animation.FuncAnimation' routine from matplotlib,
# which basically uses the 'update' function at each time frame to update the
# content of each frame. 
#
# The general form of 'tau_shift' is the following:
#
# tau_shift = frame*(time jump in 'tau_shifts' array) + (first tau in 'tau_shifts' array)
# 
# where the 'tau_shifts' array is the one introduced in the 'conditional_sampling' function.
#
# NOTE: it's up to the user to set the proper form of 'tau_shift', given the 'tau_shifts'
# array used in the computing of the C.A.s

def update(frame):

    ax.clear()
    
    tau_shift = frame*400 - 100000
    set_name = 'Medie_condizionali_10_0'
    
    filepath = set_name + '/' + str(tau_shift)
    pos = np.loadtxt(path + '/Programmi/Analisi condizionale/giusti10_DA_USARE.txt')
    means = np.loadtxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt')
    
    xpos = pos[:, 3]
    ypos = pos[:, 4]
    X, Y = np.meshgrid(xside, yside)
    # z = means[:, 1]
    z = means
    grid_z0 = griddata((xpos, ypos), z, (X, Y), method='linear')

    im = ax.imshow(grid_z0, interpolation = 'hamming', origin = 'lower',
              extent = (-85, 75, -85, 85),
              aspect = 'auto', cmap = 'Spectral',
              norm=colors.PowerNorm(vmin = -50., vmax = +3., gamma=3))
    ax.plot(xpos, ypos, 'ok', alpha=0.5, markersize=2)
    ax.plot(0, 0, 'X', color='white', markersize=10)
    ax.set_xlabel('R [cm]')
    ax.set_ylabel('Z [cm]')
    ax.set_title(rf'$<V_M>_C$ at $\tau$ = {tau_shift:.2f} [$\mu$s]')
    ax.minorticks_on()
    ax.grid()

    # Update on the progress of computation
    print(frame, end = '\r')
