import os


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the View to the Controller
        # self.view.controller = self

    def load_audio(self, file_path):
        self.model.file_path = file_path
        self.view.update_filename_label(os.path.basename(file_path))
        time, waveform, length = self.model.load_audio()

        self.view.display_time_value(time)
        # self.view.update_rt60_label()
        self.view.update_waveform_plot(waveform, length)

        self.view.display_highest_freq(self.model.compute_resonance())

        self.compute_rt60_for_frequencies(file_path)

        # self.view.update_filename_label(os.path.basename(dst))
        # self.view.update_rt60_label(sample_data['rt60'])
        # self.view.update_waveform_plot(sample_data['waveform'])
        # self.view.update_additional_plot(sample_data['additional_data'])

    def compute_rt60_for_frequencies(self, file_path):
        rt60_low, rt60_medium, rt60_high = self.model.compute_rt60_for_frequencies()

        self.view.update_rt60_plot(file_path)

