import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("")

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Load Button
        self.load_button = tk.Button(self.root, text="Load Audio", command=self.load_sample)
        self.load_button.pack(pady=10)

        # Display RT60
        self.rt60_label = tk.Label(self.root, text="RT60 Value:")
        self.rt60_label.pack(pady=5)

        # Waveform Plot
        self.waveform_canvas = tk.Canvas(self.root, width=400, height=200)
        self.waveform_canvas.pack(pady=10)

        # Additional Plots
        self.additional_canvas = tk.Canvas(self.root, width=400, height=200)
        self.additional_canvas.pack(pady=10)

    def load_sample(self):
        # Open file dialog for selecting audio file
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))

        if file_path:
            # Checks if the file type is mp3
            if os.path.splitext(file_path)[1].lower() == '.mp3':
                # Converts the file to wav
                src = file_path
                dst = os.path.splitext(file_path)[0] + '.wav'
                print("Converting...")

                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")

                # Call a function to process the selected file (you'll need to implement this)
                sample_data = self.process_audio_file(dst)

                # Update RT60 label
                self.rt60_label.config(text=f"RT60 Value: {sample_data['rt60']} seconds")

                # Update Waveform Plot
                self.plot_waveform(sample_data['waveform'], self.waveform_canvas)

                # Update Additional Plot
                self.plot_additional(sample_data['additional_data'], self.additional_canvas)

            else:
                # Call a function to process the selected file (you'll need to implement this)
                sample_data = self.process_audio_file(file_path)

                # Update RT60 label
                self.rt60_label.config(text=f"RT60 Value: {sample_data['rt60']} seconds")

                # Update Waveform Plot
                self.plot_waveform(sample_data['waveform'], self.waveform_canvas)

                # Update Additional Plot
                self.plot_additional(sample_data['additional_data'], self.additional_canvas)

    def process_audio_file(self, file_path):
        # Placeholder for processing the audio file and extracting relevant data
        # You should implement this function based on your specific requirements
        # You might use libraries like LibROSA or other audio processing tools
        # Return a dictionary containing processed data (e.g., rt60, waveform, additional_data)
        return {'rt60': 0.8, 'waveform': [0.1, 0.3, 0.5, 0.8, 1.0], 'additional_data': [0.2, 0.4, 0.6, 0.9, 1.2]}

    def plot_waveform(self, data, canvas):
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="blue")  # Placeholder line for waveform

    def plot_additional(self, data, canvas):
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="green")  # Placeholder line for additional plot


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
