#---------- Search of the proper condition on the reference probe

# def mia_gauss (x, mean, std, A):
#     esp = -(x - mean)**2 / (2*std**2)
#     return A*np.exp(esp)

# hist, bin_edges = np.histogram(ref, bins='auto')   # Bins the data in 'ref'
# x_scale = bin_edges[:-1]
# plt.plot(x_scale, hist, label=f'Set {i}')
# mean = np.mean(ref)
# std = np.std(ref)

# popt, pcov = curve_fit(mia_gauss, x_scale, hist, p0=[mean, std, 12000])

# plt.plot(x_scale, mia_gauss(x_scale, *popt), 'r', label=f'Gaussian Fit\nMean: {popt[0]:.2f}\nStd: {popt[1]:.2f}')
# plt.axvline(mean+std, 0, np.max(hist), color='k', linestyle='--', label=r'$\mu$ $\pm$ $\sigma$')
# plt.axvline(mean-std, 0, np.max(hist), color='k', linestyle='--')
# plt.axvline(mean, 0, np.max(hist), color='g', linestyle='-')
# plt.axvline(mean+1.5*std, 0, np.max(hist), color='m', linestyle='--', label=r'$\mu$ $\pm$ $1.5\sigma$')
# plt.axvline(mean+2.0*std, 0, np.max(hist), color='orange', linestyle='--', label=r'$\mu$ $\pm$ $2.0\sigma$')
# plt.axvline(mean+2.5*std, 0, np.max(hist), color='r', linestyle='--', label=r'$\mu$ $\pm$ $2.5\sigma$')
# plt.axvline(mean+3.0*std, 0, np.max(hist), color='blue', linestyle='--', label=r'$\mu$ $\pm$ $3.0\sigma$')
# plt.legend()
# plt.grid()





#-------------------- Computations of the Conditional Averages --------------------

#---------- Simple mean for NO TRIGGER VALUES

# all_mean = np.zeros(171)

# j = 0
# for i in range(0, 172):
#     if i==9:
#         continue
#     print(f"Status: i = {i}/171 and j = {j}/171", end="\r")
        
#     filename = path + ppath + '/' + f'{i}.txt'
#     data = np.loadtxt(filename)
    
#     all_mean[j] = np.mean(data[:, 2])
#     j += 1
    
# set_name = 'Medie_condizionali_10_4'
# filepath = set_name + '/No_ref'
# np.savetxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt', all_mean)

#---------- Graph for NO TRIGGER VALUES

# set_name = 'Medie_condizionali_10_4'
# filepath = set_name + '/No_ref'
# pos = np.loadtxt(path + '/Programmi/Analisi condizionale/giusti10_DA_USARE.txt')
# means = np.loadtxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt')
        
# xpos = pos[:, 3]
# ypos = pos[:, 4]
# xside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70]
# yside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
# X, Y = np.meshgrid(xside, yside)

# z = means

# grid_z0 = griddata((xpos, ypos), z, (X, Y), method='linear')

# plt.imshow(grid_z0, interpolation = 'hamming', origin = 'lower',
#            extent = (-85, 75, -85, 85),
#            aspect = 'auto', cmap = 'Spectral', vmin = -50., vmax = +3)
    
# plt.plot(xpos, ypos, 'ok', alpha=0.5, markersize=2)
# plt.plot(0, 0, 'X', color='white', markersize=10)
# plt.colorbar().set_label('$V_F$', fontsize=16)
# plt.xlabel('R [cm]')
# plt.ylabel('Z [cm]')
# plt.title(rf'Pure average of $V_M$')
# plt.minorticks_on()
# plt.grid()






#------------------- Measuring probe with some triggering:
# 
# The 'all_means' array will store all the C.A. values, thus it should be
# defined by the user: rows = number of tau_shifts, cols = number of grid pts
#
# NOTE: this is obvious, but the following parameters and definitions should be changed
#       each time different conditions are required:
#       
#       - all_means: change its size
#       - tahu_shifts: change its content
#       - filename: make sure to load the correct data!
#       - low_bound and high_bound: condition of triggering
#       - t_index: index that links the tau value and its position in 'all_means'
#       - filepath: make sure to save the results in the correct folder!

all_means = np.zeros((501, 171))   # Each row is a time-step and contains all 171 pts
# all_means = np.zeros((3, 171))

tau_shifts = np.linspace(-100000, 100000, 501)
# tau_shifts = [-100, 0, 100]
tau_shifts = tau_shifts.astype(int)

j = 0   # Index introduced to treat the misalignment between indexes and file names

for i in range(0, 172):   # For each of the grid points in the poloidal section
    
    if i==9:   # Missing file '9.txt', for this reason I introduce the index 'j'
        continue
    
    print(f"Status: i = {i}/171 and j = {j}/171", end="\r")
    
    # Load the data
    filename = path + ppath + '/' + f'{i}.txt'
    data = np.loadtxt(filename)
    ref = data[:, 1]   # Reference probe
    meas = data[:, 2]   # Measuring probe
    
    means = conditional_sampling(ref, meas, 
                                 low_bound=-np.inf, high_bound=+np.inf, 
                                 use_std=True, tau_shifts=tau_shifts)
    
    all_means[:, j] = means
    j += 1

# Save the computed C.A.s

set_name = 'Medie_condizionali_10_0'

for tau in tau_shifts:
    
    # General formula for the t_index, when the 'tau_shifts' array is symmetric to 0:
    #
    # t_index = int((tau + highest tau_shift) / (distance between two tau_shifts))
    
    t_index = int((tau + 100000)/400)   
    # t_index = int((tau + 100)/100)
    filepath = set_name + '/' + str(tau)
    np.savetxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt', all_means[t_index])
