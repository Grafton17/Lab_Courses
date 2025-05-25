# EXAMPLE: 
# the used data array is called 'E' and refers to the time evolution of the electric field.
# Specifically, it was computed with the help of the ZPIC code (see here: https://github.com/ricardo-fonseca/zpic)
#
# E[0] refers to E's time evolution at position x = 0
# E[199] refers to E's time evolution at position x = 199
#
# An example of E is loaded into the "Dispersion Relation" directory as "Example_E.txt"

# Please note, at that time I wasn't familiar with the pcolormesh function,
# therefore the drawing is pretty cumbersome. For example, I used a strange log scale
# instead of using a logarithimic coloring scheme as done in the 'Conditional Sampling' code...


binning = 401
histo = np.zeros((320, binning))
dist = 100

f = fftshift(fftfreq(320, 0.5))
k = np.linspace(-0.033, +0.033, binning)
delta_f = f[1] - [0]
delta_k = k[1] - k[0]

t = np.linspace(0, 8000, 16000)
f = fftshift(fftfreq(320, t[1] - t[0]))

start_ind = 0
finish_ind = 320

while (finish_ind <= 15999):

    x = E[0, start_ind:finish_ind]
    y = E[199, start_ind:finish_ind]
    X = fftshift(fft(x))
    Y = fftshift(fft(y))

    histo = built_histo(histo, X, Y, dist, delta_f, delta_k, binning)

    start_ind += 160
    finish_ind += 160
    # print(finish_ind)

# print(histo)

plt.figure(figsize=(8, 6))
plt.pcolormesh(k/0.02, f[160:]*2*np.pi, 10 *
               np.log10(histo[160:] + 1e-20), shading='nearest')
# plt.axhline(1, -1, 1, color='r', linestyle='--')
plt.title(rf"$f\,(k)$ relation ---  $\alpha = ${nr}")
plt.ylabel(r"$f$ / $f_{plasma}$")
plt.xlabel(r"$k\cdot u_{beam}$ / $\omega_{plasma}$")
plt.colorbar().set_label(r"$log_{10}(\sum S_n^{(j)})$")

# plt.savefig(path + ppath + f"/2_punti_alfa={nr}.png")
# plt.savefig(path + ppath + f"/2_punti_alfa={nr}.pdf")

plt.xlim(0, 1.52)

# plt.savefig(path + ppath + f"/2_punti_alfa={nr}_zoom.png")
# plt.savefig(path + ppath + f"/2_punti_alfa={nr}_zoom.pdf")
