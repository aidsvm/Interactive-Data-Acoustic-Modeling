from tkinter import filedialog

class Model:
    def __init__(self, filename):
        self.filename = filename
        
        @property
        def filename(self):
            return self.__filename

        @filename.setter
        def filename(self, value):
            filepath =



