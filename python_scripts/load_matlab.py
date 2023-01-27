import numpy as np

from scipy.io import loadmat
import mne, glob

dat = loadmat("../matlab_data/s02.mat")

print(dat['eeg'][0][0])