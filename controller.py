import os


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio(self, file_path):
        # Set the file path in the model
        self.model.file_path = file_path

        # Update the filename label in the view
        self.view.update_filename_label(os.path.basename(file_path))

        # Load audio data from the model
        time, waveform, length = self.model.load_audio()

        # Display the loaded audio information in the view
        self.view.display_time_value(time)
        self.view.change_graph()

        # Display the highest resonance frequency in the view
        self.view.display_highest_freq(self.model.compute_resonance())

    def get_waveform_length(self):
        return self.model.get_waveform_length()

    def get_waveform_data(self):
        return self.model.get_waveform_data()

    def get_file_path(self):
        return self.model.get_file_path()

    def plot_combined_rt60(self, filepath, fs, signal):
        # Low RT60
        low_rt60_db = self.compute_rt60_for_frequencies('low')
        time_axis_low, amplitude_low = self.model.plot_combined_rt60(fs, signal, low_rt60_db)

        # Mid RT60
        mid_rt60_db = self.compute_rt60_for_frequencies('mid')
        time_axis_mid, amplitude_mid = self.model.plot_combined_rt60(fs, signal, mid_rt60_db)

        # High RT60
        high_rt60_db = self.compute_rt60_for_frequencies('high')
        time_axis_high, amplitude_high = self.model.plot_combined_rt60(fs, signal, high_rt60_db)

        return time_axis_low, amplitude_low, time_axis_mid, amplitude_mid, time_axis_high, amplitude_high

    def plot_low_rt60(self, filepath, fs, signal):
        low_rt60_db = self.compute_rt60_for_frequencies('low')

        time_axis, amplitude, decay_point = self.model.plot_rt60(fs, signal, low_rt60_db)

        return time_axis, amplitude, decay_point

    def plot_mid_rt60(self, filepath, fs, signal):
        plot_mid_rt60 = self.compute_rt60_for_frequencies('mid')

        time_axis, amplitude, decay_point = self.model.plot_rt60(fs, signal, plot_mid_rt60)

        return time_axis, amplitude, decay_point

    def plot_high_rt60(self, filepath, fs, signal):
        plot_high_rt60 = self.compute_rt60_for_frequencies('high')

        time_axis, amplitude, decay_point = self.model.plot_rt60(fs, signal, plot_high_rt60)

        return time_axis, amplitude, decay_point

    def compute_rt60_for_frequencies(self, type_range):
        # Compute RT60 values for low, medium, and high frequencies
        rt60_low, rt60_medium, rt60_high = self.model.compute_rt60_for_frequencies(
            low_freq_range=(0, 100),
            medium_freq_range=(100, 1000),
            high_freq_range=(1000, None)
        )

        if type_range == 'low':
            return rt60_low
        elif type_range == 'mid':
            return rt60_medium
        elif type_range == 'high':
            return rt60_high

    def calculate_rt60_value(self, spectrum, freqs, t):
        target_frequency, rt60 = self.model.calculate_rt60_value(spectrum, freqs, t)

        return target_frequency, rt60
