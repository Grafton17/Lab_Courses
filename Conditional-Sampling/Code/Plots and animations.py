# CONDITIONAL SAMPLING: PLOTS and ANIMATION

#---------- Save the plots for each tau_shift in 'tau_shifts' array

# Different versions of 'tau_shifts':
# tau_shifts = np.linspace(-100000, 100000, 501)
# tau_shifts = [-100000]

# for tau in tau_shifts:
#     saveplot_conditional_sampling(tau_shift=tau, set_name="Prove_immagini")
    
#---------- Collate all the plts in one animation:
    
# Firstly, plot the first frame of the video. The code is exactly the same used
# in the 'saveplot_conditional_sampling' function written high above.

set_name = 'Medie_condizionali_10_0'
filepath = set_name + '/' + str(-100000)
pos = np.loadtxt(path + '/Programmi/Analisi condizionale/giusti10_DA_USARE.txt')
means = np.loadtxt(path + f'/Programmi/Analisi condizionale/Measuring probe/{filepath}.txt')

xpos = pos[:, 3]
ypos = pos[:, 4]
xside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70]
yside = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
X, Y = np.meshgrid(xside, yside)

# z = means[:, 1]
z = means

grid_z0 = griddata((xpos, ypos), z, (X, Y), method='linear')

fig, ax = plt.subplots(1, 1)

im = ax.imshow(grid_z0, interpolation = 'hamming', origin = 'lower',
          extent = (-85, 75, -85, 85),
          aspect = 'auto', cmap = 'Spectral',
          norm=colors.PowerNorm(vmin = -50., vmax = +3., gamma=3))
ax.plot(xpos, ypos, 'ok', alpha=0.5, markersize=2)
ax.plot(0, 0, 'X', color='white', markersize=10)
fig.colorbar(ax=ax, mappable = im).set_label('$V_F$', fontsize=16)
ax.set_xlabel('R [cm]')
ax.set_ylabel('Z [cm]')
ax.set_title(rf'$<V_M>_C$ at $\tau$ = {-400:.2f} [$\mu$s]')
ax.minorticks_on()
ax.grid()

# Set the parameters of the animation:
#   - nr_frames: number of frames in the video
#   - fps: frames per second of the video

nr_frames = 501
fps = 8   # 256 for .gif

ani = animation.FuncAnimation(fig = fig, func = update, frames = nr_frames, interval = 1000./fps, repeat = False)
ani.save(filename = path + '/Programmi/Analisi condizionale/Video3.mp4', writer="ffmpeg")
