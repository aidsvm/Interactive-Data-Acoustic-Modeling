import os
from pydub import AudioSegment
import model


class Controller:
    def __init__(self, root, model, view):
        self.model = model
        self.view = view

        # Connect the View to the Controller
        self.view.controller = self

    def load_sample(self, file_path):
        # Checks if the file type is mp3
        if not os.path.splitext(file_path)[1].lower() == '.wav':
            # Converts the file to wav
            src = file_path
            dst = os.path.splitext(file_path)[0] + '.wav'

            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")

            # Call the Model to process the selected file
            sample_data = self.model.process_audio_file(dst)

            # Notify the View to update UI elements
            self.view.update_filename_label(os.path.basename(dst))
            self.view.update_rt60_label(sample_data['rt60'])
            self.view.update_waveform_plot(sample_data['waveform'])
            self.view.update_additional_plot(sample_data['additional_data'])

        else:
            # Call the Model to process the selected file
            sample_data = self.model.process_audio_file(file_path)

            # Notify the View to update UI elements
            self.view.update_filename_label(os.path.basename(file_path))
            self.view.update_rt60_label(sample_data['rt60'])
            self.view.update_waveform_plot(sample_data['waveform'])
            self.view.update_additional_plot(sample_data['additional_data'])