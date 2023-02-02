import os
import numpy as np
import pandas as pd
import mne
from numpy.fft import fft
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

s_rate = 250
data = pd.read_csv("c_ExG.csv")
fft_1 = data[['ch4']].to_numpy()
n_point = fft_1.shape[0]
freq = s_rate * np.arange(int(n_point / 2)) / n_point
x = data[['ch4']].to_numpy()
ch_names = ['CH 1', 'CH 2', 'CH 3', 'CH 4']
#

S = fft(fft_1.transpose(), n=n_point) / n_point
fft_content = np.abs(S[:, range(int(n_point / 2))])
fft_content = gaussian_filter1d(fft_content, 1)
plt.plot(S.transpose())
plt.show()

f_channels = data[['ch1', 'ch2', 'ch3', 'ch4']].to_numpy()
info = mne.create_info(ch_names = ch_names, sfreq=250)
raw = mne.io.RawArray(f_channels.transpose(), info)
raw.plot(block=True)
# print(S)
S_mag = np.abs(S)
S_phase = np.angle(S)
plt.plot(S.shape[0],S_mag,'.-')
plt.plot(S.shape[0],S_phase,'.-')
plt.show()


# for proj in (False, True):
#     with mne.viz.use_browser_backend('matplotlib'):
#         fig = raw.plot(n_channels=2, proj=proj, scalings=dict(eeg=50e-6),
#                        show_scrollbars=False, block=True)
#     fig.subplots_adjust(top=0.9)  # make room for title
#     ref = 'Average' if proj else 'No'
#     fig.suptitle(f'{ref} reference', size='xx-large', weight='bold')
