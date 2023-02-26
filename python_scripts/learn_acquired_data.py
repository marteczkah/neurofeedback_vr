"""Script I used to generate the fft of the acquired data
and then create visualizations."""
import os
import numpy as np
import pandas as pd
import mne
from numpy.fft import fft
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

# readubg tge data abd setup
s_rate = 250 # sampling rate
data = pd.read_csv("../data/lefthand1_ExG.csv")
fft_1 = data[['ch4']].to_numpy() # pick the channel
n_point = fft_1.shape[0]
freq = s_rate * np.arange(int(n_point / 2)) / n_point
ch_names = ['CH 1', 'CH 2', 'CH 3', 'CH 4']

# fft based on the explorepy code
S = fft(fft_1.transpose(), n=n_point) / n_point
fft_content = np.abs(S[:, range(int(n_point / 2))])
fft_content = gaussian_filter1d(fft_content, 1)
plt.plot(fft_content.transpose())
plt.show()

# generate MNE raw array and plot it
f_channels = data[['ch1', 'ch2', 'ch3', 'ch4']].to_numpy()
info = mne.create_info(ch_names = ch_names, sfreq=250)
raw = mne.io.RawArray(f_channels.transpose(), info)
raw.plot(block=True)

# calculating and plotting the magnitude and phase of the fft
S_mag = np.abs(S)
S_phase = np.angle(S)
plt.plot(S.shape[0],S_mag,'.-')
plt.plot(S.shape[0],S_phase,'.-')
plt.show()

