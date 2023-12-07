import os


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the View to the Controller
        # self.view.controller = self

    def load_audio(self, file_path):
        # Set the file path in the model
        self.model.file_path = file_path

        # Update the filename label in the view
        self.view.update_filename_label(os.path.basename(file_path))

        # Load audio data from the model
        time, waveform, length = self.model.load_audio()

        # Display the loaded audio information in the view
        self.view.display_time_value(time)
        self.view.update_waveform_plot(waveform, length)

        # Display the highest resonance frequency in the view
        self.view.display_highest_freq(self.model.compute_resonance())

        # Compute and display RT60 values for different frequency ranges
        self.compute_rt60_for_frequencies(file_path)

    def compute_rt60_for_frequencies(self, file_path):
        # Compute RT60 values for low, medium, and high frequencies
        rt60_low, rt60_medium, rt60_high = self.model.compute_rt60_for_frequencies(
            low_freq_range=(0, 100),
            medium_freq_range=(100, 1000),  # Ensure this tuple is correctly defined
            high_freq_range=(1000, None)
        )

        # Update the RT60 plot in the view
        self.view.update_spectrogram(file_path)

        # Optionally, update RT60 labels in the view if needed
        # self.view.update_rt60_label(rt60_low, rt60_medium, rt60_high)

        # Plot frequency ranges on the GUI
        self.view.plot_frequency_ranges(rt60_low, rt60_medium, rt60_high)

    def show_waveform(self):
        if not self.view.current_graph == "spectrogram":
            # Hide the spectrogram if it's currently displayed
            self.view.hide_spectrogram()

        # Update the waveform in the view
        self.view.update_waveform_plot(self.model.get_waveform_data(), self.model.get_waveform_length())

    def show_spectrogram(self):
        if not self.view.current_graph == "waveform":
            # Hide the waveform if it's currently displayed
            self.view.hide_waveform()

        # Update the spectrogram in the view
        self.view.update_spectrogram(self.model.get_file_path())
