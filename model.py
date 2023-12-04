from tkinter import filedialog
import soundfile as sf

class Model:
    def __init__(self, filename):
        self.filename = filename
        
        @property
        def filename(self):
            return self.__filename

        @filename.setter
        def filename(self, filepath):
            if filepath:
                data, sample_rate = sf.read(filepath)




