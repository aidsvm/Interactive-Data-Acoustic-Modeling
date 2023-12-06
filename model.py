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
