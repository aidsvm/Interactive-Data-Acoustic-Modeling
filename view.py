import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create and place widgets
        # Load Button
        self.load_button = tk.Button(self, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=1, column=1, pady=10)

        # Filename Label
        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=2, column=1)

        # Display RT60
        self.rt60_label = tk.Label(self, text="")
        self.rt60_label.grid(row=10, column=1, pady=10)

        # RT60 Plots for Low, Medium, High Frequencies
        self.rt60_canvas = tk.Canvas(self, width=400, height=200)
        self.rt60_canvas.grid(row=15, column=10, pady=10)

        # Waveform Plot
        self.waveform_canvas = tk.Canvas(self, width=400, height=200)
        self.waveform_canvas.grid(row=15, column=1, pady=10)

        # Graphs the waveform to the GUI
        self.fig_waveform = Figure(figsize=(7, 5), dpi=100)
        self.ax_waveform = self.fig_waveform.add_subplot(111)
        self.canvas_waveform = FigureCanvasTkAgg(self.fig_waveform, master=self.waveform_canvas)
        self.canvas_waveform.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.rt60_fig_waveform = Figure(figsize=(7, 5), dpi=100)
        self.rt60_ax_waveform = self.rt60_fig_waveform.add_subplot(111)
        self.rt60_canvas_waveform = FigureCanvasTkAgg(self.rt60_fig_waveform, master=self.rt60_canvas)
        self.rt60_canvas_waveform.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Highest freq
        self.highest_res_freq_label = tk.Label(self, text="")
        self.highest_res_freq_label.grid(row=17, column=1, pady=10)

        # Total time of audio file
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=18, column=1, pady=5)

        # Additional Plots
        self.additional_canvas = tk.Canvas(self, width=400, height=200)
        self.additional_canvas.grid(row=19, column=1, pady=10)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def load_audio(self):
        # Open file dialog for selecting audio file
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))

        print(f"Selected file: {file_path}")  # Add this print statement

        if file_path:
            print("Calling controller.load_audio")  # Add this print statement
            # Notify the Controller about the user's action
            self.controller.load_audio(file_path)

    def display_time_value(self, time):
        self.time_label.config(text=f"Time: {time:.2f} seconds")

    def update_filename_label(self, filename):
        # Update Filename Label
        self.filename_label.config(text=f"File: {filename}")

    def update_rt60_label(self, rt60_value):
        # Update RT60 label
        self.rt60_label.config(text=f"RT60 Value: {rt60_value} seconds")

    def display_highest_freq(self, highest_res_freq):
        self.highest_res_freq_label.config(text=f"Highest Resonance Frequency: {highest_res_freq:.2f} Hz")

    def update_waveform_plot(self, waveform_data, length):
        # Update Waveform Plot
        self.plot_waveform(waveform_data, length)

    def update_additional_plot(self, additional_data, time):
        # Update Additional Plot
        self.plot_additional(additional_data, time)

    def update_rt60_plot(self, file_path):
        self.plot_rt60(file_path)

# Function plots all the frequencies into one spectrogram
    def plot_rt60(self, filepath):
        self.rt60_ax_waveform.clear()
        # Read audio file
        sample_rate, data = wavfile.read(filepath)

        # Calculate the spectrogram
        spectrum, freqs, t, im = self.rt60_ax_waveform.specgram(data, Fs=sample_rate, NFFT=1024,
                                                                cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im, ax=self.rt60_ax_waveform)
        cbar.set_label('Intensity (dB)')

        # Set labels and title
        self.rt60_ax_waveform.set_xlabel('Time (s)')
        self.rt60_ax_waveform.set_ylabel('Frequency (Hz)')
        self.rt60_ax_waveform.set_title('Spectrogram')

        # Redraw the canvas
        self.rt60_canvas_waveform.draw()

    def plot_waveform(self, data, length):
        self.ax_waveform.clear()
        time = np.linspace(0., length, data.shape[0])
        self.ax_waveform.plot(time, data)
        self.ax_waveform.set_title('Wav Form')
        self.ax_waveform.set_xlabel('Time (s)')
        self.ax_waveform.set_ylabel('Amplitude')

        # Redraw the canvas
        self.canvas_waveform.draw()

    def plot_additional(self, data, canvas):
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="green")  # Placeholder line for additional plot
