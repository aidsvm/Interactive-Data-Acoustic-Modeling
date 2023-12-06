import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

# wav_fname = 'PolyHallClap_10mM.WAV'
# samplerate, data = wavfile.read(wav_fname)
# print(f"number of channels = {data.shape[len(data.shape) - 1]}")
# print(f"sample rate = {samplerate}Hz")
# length = data.shape[0] / samplerate
# print(f"length = {length}s")


sample_rate, data = wavfile.read('PolyHallClap_10mM.WAV')
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate,
                                      NFFT=1024, cmap=plt.get_cmap('autumn_r'))
cbar = plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity (dB)')
plt.show()