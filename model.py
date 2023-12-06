import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment
from scipy.signal import find_peaks


class Model:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.sample_rate = None
        self.mono_data = None

    def load_audio(self):
        if not os.path.splitext(self.file_path)[1].lower() == '.wav':
            # Converts the file to wav
            src = self.file_path
            dst = os.path.splitext(self.file_path)[0] + '.wav'

            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")

            # Call the Model to process the selected file
            time, waveform, length = self.process_audio_file(dst)

            return time, waveform, length

        else:
            # Call the Model to process the selected file
            time, waveform, length = self.process_audio_file(self.file_path)

            return time, waveform, length

    def process_audio_file(self, filepath):
        if filepath:
            self.data, self.sample_rate = sf.read(filepath)

            if len(self.data.shape) > 1:
                self.mono_data = np.mean(self.data, axis=1)

            else:
                self.mono_data = self.data

            duration = len(self.mono_data) / self.sample_rate
            length = self.data.shape[0] / self.sample_rate

            return duration, self.mono_data, length

    def compute_resonance(self):
        spectrum = np.fft.fft(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)

        positive_frequencies = frequencies[:len(frequencies) // 2]
        positive_spectrum = spectrum[:len(spectrum) // 2]

        max_index = np.argmax(np.abs(positive_spectrum))

        highest_res_freq = positive_frequencies[max_index]

        return highest_res_freq

    def compute_rt60_for_frequencies(self):
        spectrum = np.fft.fft(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)

        # Define frequency ranges
        low_freq_range = (0, 100)  # Adjust these values as needed
        medium_freq_range = (100, 1000)
        high_freq_range = (1000, self.sample_rate / 2)

        # Find indices corresponding to each frequency range
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        medium_freq_indices = np.where((frequencies >= medium_freq_range[0]) & (frequencies < medium_freq_range[1]))[0]
        high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        return frequencies[low_freq_indices], frequencies[medium_freq_indices], frequencies[high_freq_indices]

