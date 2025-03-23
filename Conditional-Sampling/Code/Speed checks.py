# This script was used to compare the two proposed solutions in the computation of
# the conditional mean values. 
#
# The difference can be barely seen and, at the end of the day, what takes time
# is the .txt loading from memory, thus the computation is performed for 
# all tau_shifts for each space point before passing to the next one.
# 
# In this manner, the .txt loading is reduced to the minimum.

import timeit
setup = '''
import numpy as np
path = 'C:/Users/sebis/'\
       'OneDrive - Università degli Studi di Milano-Bicocca/4anno/'\
       'Fisica dei Plasmi I - Zerbi/Parte 2/Esperienze/Turbolenza'
# ppath = '/Dati/Analisi Condizionale/Analisi condizionale parte centrale con risoluzione 5 mm'
ppath = '/Dati/Analisi Condizionale/Analisi condizionale risoluzione 10 mm'

def conditional_sampling(ref, meas, low_bound = -np.inf, high_bound = np.inf, use_std = True):
    
    mean = np.mean(ref)
    std = np.std(ref, ddof=1, mean=mean)   # ddof=1 uses Bessel's correction
    
    if (use_std==True):
        low_bound = low_bound*std + mean
        high_bound = high_bound*std + mean
    
    # Use np.where()
    # cond_meas = np.where(low_bound < ref, np.where(ref < high_bound, meas, 0), 0)
    cond_ref  = np.where(low_bound < ref, np.where(ref < high_bound, ref,  0), 0)
    
    # Use boolean indexing, which seems to be faster than np.where()
    ref[ref < low_bound] = 0
    ref[ref > high_bound] = 0
    cond_meas2 = meas.copy()
    cond_meas2[ref == 0] = 0
    # print(f"{np.array_equal(cond_meas, cond_meas2)}")   # <--- They are indeed equal!
    
    # j = 230000
    # plt.plot(time[j:j+10000], ref[j:j+10000], label='Original')
    # plt.plot(time[j:j+10000], cond_ref[j:j+10000], label='Filtered')
    # plt.legend()
    # plt.grid()
    # plt.axhline(low_bound, color='k')
    # plt.axhline(high_bound, color='k')
    
    return cond_meas2, cond_ref

for i in range(0, 1):
    if i==9:
        continue
    
    filename = path + ppath + '/' + f'{i}.txt'
    data = np.loadtxt(filename)
    
    time = data[:, 0]
    ref = data[:, 1]   # Reference probe
    meas = data[:, 2]   # Measuring probe
    
    cond_meas, cond_ref = conditional_sampling(ref, meas, low_bound=2, high_bound=3, use_std=True)
'''

print(min(timeit.Timer(setup=setup).repeat(7, 1000)))

