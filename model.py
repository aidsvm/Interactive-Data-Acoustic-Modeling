import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment


class Model:
    def __init__(self, file_path):
        # Initialize the Model with the given file path
        self.length = None
        self.waveform = None
        self.file_path = file_path
        self.data = None
        self.sample_rate = None
        self.mono_data = None

    def get_waveform_data(self):
        return self.waveform

    def get_waveform_length(self):
        return self.length

    def get_file_path(self):
        return self.file_path

    def load_audio(self):
        # Check if the file is in WAV format; if not, convert it
        if not os.path.splitext(self.file_path)[1].lower() == '.wav':
            # Convert the file to WAV format
            src = self.file_path
            dst = os.path.splitext(self.file_path)[0] + '.wav'
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")

            # Process the selected file
            time, self.waveform, self.length = self.process_audio_file(dst)

            return time, self.waveform, self.length

        else:
            # Process the selected file
            time, self.waveform, self.length = self.process_audio_file(self.file_path)

            return time, self.waveform, self.length

    def process_audio_file(self, filepath):
        # Process the audio file and return relevant information
        if filepath:
            self.data, self.sample_rate = sf.read(filepath)

            if len(self.data.shape) > 1:
                self.mono_data = np.mean(self.data, axis=1)
            else:
                self.mono_data = self.data

            duration = len(self.mono_data) / self.sample_rate
            self.length = self.data.shape[0] / self.sample_rate

            return duration, self.mono_data, self.length

    def compute_resonance(self):
        # Compute and return the highest resonance frequency
        spectrum = np.fft.fft(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)
        positive_frequencies = frequencies[:len(frequencies) // 2]
        positive_spectrum = spectrum[:len(spectrum) // 2]

        max_index = np.argmax(np.abs(positive_spectrum))
        highest_res_freq = positive_frequencies[max_index]

        return highest_res_freq

    def compute_rt60_for_frequencies(self, low_freq_range=(0, 100), medium_freq_range=(100, 1000),
                                     high_freq_range=(1000, None)):

        # Normalize the spectrum
        spectrum = np.fft.fft(self.mono_data) / len(self.mono_data)
        frequencies = np.fft.fftfreq(len(self.mono_data), 1 / self.sample_rate)

        # Find indices corresponding to each frequency range
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        medium_freq_indices = np.where((frequencies >= medium_freq_range[0]) & (frequencies < medium_freq_range[1]))[0]

        # Handle the case where high_freq_range[1] is None
        if high_freq_range[1] is None:
            high_freq_indices = np.where((frequencies >= high_freq_range[0]))[0]
        else:
            high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        return frequencies[low_freq_indices], frequencies[medium_freq_indices], frequencies[high_freq_indices]

    def plot_combined_rt60(self, fs, signal, rt60_db):
        time_axis = np.arange(0, len(signal)) / fs
        if len(rt60_db) != len(time_axis):
            rt60_db = np.interp(time_axis, np.linspace(0, 1, len(rt60_db)), rt60_db)
        amplitude = np.exp(-rt60_db / 20 * time_axis)

        return time_axis, amplitude

    def plot_rt60(self, fs, signal, rt60_db):
        time_axis = np.arange(0, len(signal)) / fs
        if len(rt60_db) != len(time_axis):
            rt60_db = np.interp(time_axis, np.linspace(0, 1, len(rt60_db)), rt60_db)
        amplitude = np.exp(-rt60_db / 20 * time_axis)
        threshold = -60
        decay_point = np.argmax(amplitude <= threshold)

        return time_axis, amplitude, decay_point

    def calculate_rt60_value(self, spectrum, freqs, t):
        def find_target_frequency(freqs):
            global x
            for x in freqs:
                if x > 1000:
                    break
            return x

        def frequency_check(spectrum, freqs):
            target_frequency = find_target_frequency(freqs)
            index_of_frequency = np.where(freqs == target_frequency)[0][0]
            # find sound data for a particular frequency
            data_for_frequency = spectrum[index_of_frequency]
            # change a digital signal for values in decibels
            data_in_db_fun = 10 * np.log10(data_for_frequency)
            return data_in_db_fun

        data_in_db = frequency_check(spectrum, freqs)

        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]

        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0]

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0]

        rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
        rt60 = 3 * rt20

        target_frequency = find_target_frequency(freqs)

        return target_frequency, rt60
