import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment


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
            time, waveform = self.process_audio_file(dst)

            return time, waveform

            # Notify the View to update UI elements
            self.view.update_filename_label(os.path.basename(dst))
            self.view.update_rt60_label(sample_data['rt60'])
            self.view.update_waveform_plot(sample_data['waveform'])
            self.view.update_additional_plot(sample_data['additional_data'])

        else:
            # Call the Model to process the selected file
            time, waveform = self.process_audio_file(self.file_path)

            return time, waveform

            # Notify the View to update UI elements
            self.view.update_filename_label(os.path.basename(self.file_path))
            self.view.update_rt60_label(sample_data['rt60'])
            self.view.update_waveform_plot(sample_data['waveform'])
            self.view.update_additional_plot(sample_data['additional_data'])

    def process_audio_file(self, filepath):
        if filepath:
            self.data, self.sample_rate = sf.read(filepath)

            if len(self.data.shape) > 1:
                self.mono_data = np.mean(self.data, axis=1)

            else:
                self.mono_data = self.data

            duration = len(self.mono_data) / self.sample_rate

            return duration, self.mono_data