import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft

data = pd.read_csv("../data_january_6th/max_right_movement_ExG.csv")
x = data['ch3'].to_numpy()
x = x[:1250]

# sampling rate
sr = 250
# sampling interval
ts = 1.0/sr
t = np.arange(0,5,ts)

X = fft(x)
print(X.max())
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T

plt.figure(figsize = (15, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 20)

plt.subplot(122)
plt.plot(t, ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

# plt.figure(figsize = (15, 8))
# plt.plot(t, x, 'r')
# plt.ylabel('Amplitude')
#
# plt.show()