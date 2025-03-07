# I create a wave coupled signal, where 5 and 10 [kHz] wave interact to give a 15 [kHz] wave.
# Furthermore, I add some random normal noise to make the surrogate signal more real.
# 
# In the absence of a random noise, the plot shows a strong bi-coherence for all frequencies 
# coupled with 5, 10 and 15 [kHz] respectively. That's due to the frequency leakage phenomenon,
# in which the frequency content of the 5, 10 and 15 [kHz] leaks to neighboring bins. 
#
# This leaks maintain the same phase of original bins, thus it is as our starting signal was
# made up of all frequencies (where 5, 10 and 15 dominates all over the others), which are all coupled. 
# The coupling strength is thus different and scales as follows:
#   - low coupling: between two polluted bins
#   - high coupling: between one polluted bin and one of the original bins (5, 10 or 15 [kHz])
#   - really high coupling: between two original bins (5, 10 or 15 [kHz])
#
# An example of the leakage phenomenon can be seen in 'Bi-coherence_example_no_noise.png'
# An example of the noisy signal can be seen in 'Bi-coherence_example.png'

full_time = np.linspace(1e-6, 1, 1000000)   # A signal of length 1 sec with 1 [MHz] of sampling rate

time = full_time[::8]
dt = time[1] - time[0]

ref = (100*np.sin(0.5*2*cst.pi*time*10**4) + 100*np.sin(2*cst.pi*time*10**4) +
      100*np.sin(1.5*2*cst.pi*time*10**4) + np.random.normal(0, 30, len(time)))   # Noisy signal

# ref = (100*np.sin(0.5*2*cst.pi*time*10**4) + 100*np.sin(2*cst.pi*time*10**4) +
#       100*np.sin(1.5*2*cst.pi*time*10**4))   # No noise signal

B, b, f = compute_bicoherence(ref, fs=1/dt, win_len=9999, win_hop=1000, f_hop=1)
plot_bicoherence(b, f, win_len=9999)

'''
# ---------- SOME VERIFICATIONS OF THE GENERATED SIGNALS:
plt.plot(time, ref)

# ----- FFT by scipy on a full length signal

TF = fftshift(fft(ref))
F = fftshift(fftfreq(len(ref), dt))

# ----- STFT by scipy on pieces of the signal

# my_win = windows.blackman(9999)
# SFT = ShortTimeFFT(win = my_win, hop = 1000, fs = 1/dt)
# FTs = SFT.stft(ref)
# TF = FTs[:,2]
# F = SFT.f

# ----- DRAWING

plt.plot(F*10**(-3), np.abs(TF))
# plt.plot(F, np.real(TF))
# plt.plot(F, np.imag(TF))
plt.grid()
plt.axvline(5,0,100)
'''
