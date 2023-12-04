from tkinter import filedialog
import soundfile as sf
import numpy as np


def open_file():
    filepath = filedialog.askopenfilename(title="Please select a .wav file.",
                                          filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
    return filepath


class Model:
    def __init__(self):
        self.filepath = None
        self.data = None
        self.sample_rate = None
        self.mono_data = None

    def read_wav_file(self):
        if self.filepath:
            self.data, self.sample_rate = sf.read(self.filepath)

            if len(self.data.shape) > 1:
                self.mono_data = np.mean(self.data, axis=1)

            else:
                self.mono_data = self.data

            duration = len(self.mono_data) / self.sample_rate
            print(f"Duration: {duration:.2f} seconds")

    def run(self):

        self.filepath = open_file()
        self.read_wav_file()
