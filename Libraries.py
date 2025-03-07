import sys
import os
import fnmatch
# np.set_printoptions(threshold=sys.maxsize)

import numpy as np
import scipy.constants as cst
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Signal analysis
from scipy.fft import fft, ifft, fftshift, fftfreq
from scipy.signal import spectrogram, csd, welch, coherence, savgol_filter
from scipy.signal import ShortTimeFFT, windows   # They are a class and a suite
from scipy.optimize import curve_fit
from scipy.stats import skew, kurtosis

import pybispectra
from pybispectra import get_example_data_paths
from pybispectra.utils import compute_fft
from pybispectra.cfc import PAC
from pybispectra.general import Bispectrum   # It's a class

import cmath

# Useful for animations' making of
import matplotlib.animation as animation
from IPython import display

# Modify plots's configurations during the runtime
mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13
mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['legend.fontsize'] = 16
mpl.rcParams['figure.figsize'] = (8, 6)
