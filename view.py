import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile


# Define the View class responsible for the GUI components
class View(ttk.Frame):
    def __init__(self, parent):
        # Initialize the GUI components
        super().__init__(parent)

        # Create and place widgets
        # Load Button
        self.load_button = tk.Button(self, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=0, column=0, pady=10)

        # Graph functions for switching between graphs
        self.graph_functions = [
            self.plot_waveform,
            self.plot_low_rt60,
            self.plot_mid_rt60,
            self.plot_high_rt60,
            self.plot_spectrogram
        ]
        self.graph_index = 0

        # Matplotlib figure and canvas for displaying graphs
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.canvas.draw()

        # Button to change graph
        self.change_graph_button = tk.Button(self, text="Switch Graph", command=self.change_graph)
        self.change_graph_button.grid(row=3, column=0, pady=10)

        # Button to combine frequencies
        self.combine_button = tk.Button(self, text="Combine Frequencies", command=self.combine_frequencies)
        self.combine_button.grid(row=3, column=0, pady=10, sticky=tk.E)

        # Filename Label
        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=1, column=0)

        # Display RT60
        self.rt60_label = tk.Label(self, text="")
        self.rt60_label.grid(row=2, column=1, pady=10)

        # Highest freq
        self.highest_res_freq_label = tk.Label(self, text="")
        self.highest_res_freq_label.grid(row=5, column=0, pady=10)

        # Total time of audio file
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=6, column=0, pady=5)

        # Variables for storing spectrogram data
        self.spectrum = None
        self.freqs = None
        self.t = None

        # set the controller
        self.controller = None

    def reset_canvas(self):
        # Reset the Matplotlib canvas
        self.ax.clear()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.canvas.draw()

    def set_controller(self, controller):
        # Set the controller for communication
        self.controller = controller

    def load_audio(self):
        # Open file dialog for selecting audio file
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if file_path:
            # Notify the Controller about the user's action
            self.controller.load_audio(file_path)

    def change_graph(self):
        # Reset the canvas and RT60 label
        self.reset_canvas()
        self.rt60_label.config(text="")

        # Call the next graph function
        current_function = self.graph_functions[self.graph_index]
        current_function()

        # Increment the index for the next click
        self.graph_index = (self.graph_index + 1) % len(self.graph_functions)

        # Redraw the canvas with the new graph
        self.canvas.draw()

    def display_time_value(self, time):
        # Display time value on the GUI
        self.time_label.config(text=f"Time: {time:.2f} seconds")

    def update_filename_label(self, filename):
        # Update Filename Label
        self.filename_label.config(text=f"File: {filename}")

    def display_highest_freq(self, highest_res_freq):
        # Display the highest resonance frequency on the GUI
        self.highest_res_freq_label.config(text=f"Highest Resonance Frequency: {highest_res_freq:.2f} Hz")

    def plot_waveform(self):
        # Plot waveform on the GUI
        length = self.controller.get_waveform_length()
        data = self.controller.get_waveform_data()

        # Plot waveform on the GUI
        self.ax.clear()
        time = np.linspace(0, length, data.shape[0])
        self.ax.plot(time, data)
        self.ax.set_title('Waveform')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.canvas.draw()

    def plot_combined_rt60(self):
        # Plot combined RT60 for low, mid, and high frequency ranges
        self.reset_canvas()

        filepath = self.controller.get_file_path()

        fs, signal = wavfile.read(filepath)

        time_axis_low, amplitude_low, time_axis_mid, amplitude_mid, time_axis_high, amplitude_high = \
            (self.controller.plot_combined_rt60(filepath, fs, signal))

        self.ax.plot(time_axis_low, 20 * np.log10(amplitude_low), label='Low RT60 Decay Curve')
        self.ax.plot(time_axis_mid, 20 * np.log10(amplitude_mid), label='Mid RT60 Decay Curve')
        self.ax.plot(time_axis_high, 20 * np.log10(amplitude_high), label='High RT60 Decay Curve')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('Combined Reverberation Time Calculation')
        self.ax.legend()

    def combine_frequencies(self):
        # Clear the current graph
        self.ax.clear()

        # Call the combined RT60 graph function
        self.plot_combined_rt60()
        if self.spectrum is None and self.freqs is None and self.t is None:
            self.rt60_label.config(text="RT60 Value: Please showcase all graphs first!", fg="red")
        else:
            self.update_rt60_label(self.spectrum, self.freqs, self.t)

        # Redraw the canvas with the new graph
        self.canvas.draw()

    def plot_low_rt60(self):
        # Plot RT60 for the low frequency range
        filepath = self.controller.get_file_path()

        fs, signal = wavfile.read(filepath)

        time_axis, amplitude, decay_point = self.controller.plot_low_rt60(filepath, fs, signal)

        self.ax.plot(time_axis, 20 * np.log10(amplitude), label='Decay Curve')

        self.ax.scatter(time_axis[decay_point], 20 * np.log10(amplitude[decay_point]), color='red',
                        label='60 dB Decay Point')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('Low Reverberation Time Calculation')
        self.ax.legend()

    def plot_mid_rt60(self):
        # Plot RT60 for the mid frequency range
        filepath = self.controller.get_file_path()

        fs, signal = wavfile.read(filepath)

        time_axis, amplitude, decay_point = self.controller.plot_mid_rt60(filepath, fs, signal)

        self.ax.plot(time_axis, 20 * np.log10(amplitude), label='Decay Curve')

        self.ax.scatter(time_axis[decay_point], 20 * np.log10(amplitude[decay_point]), color='red',
                        label='60 dB Decay Point')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('Mid Reverberation Time Calculation')
        self.ax.legend()

    def plot_high_rt60(self):
        # Plot RT60 for the high frequency range
        filepath = self.controller.get_file_path()

        fs, signal = wavfile.read(filepath)

        time_axis, amplitude, decay_point = self.controller.plot_high_rt60(filepath, fs, signal)

        self.ax.plot(time_axis, 20 * np.log10(amplitude), label='Decay Curve')

        self.ax.scatter(time_axis[decay_point], 20 * np.log10(amplitude[decay_point]), color='red',
                        label='60 dB Decay Point')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('High Reverberation Time Calculation')
        self.ax.legend()

    def plot_spectrogram(self):
        filepath = self.controller.get_file_path()

        # Plot spectrogram on the GUI
        sample_rate, data = wavfile.read(filepath)
        self.spectrum, self.freqs, self.t, im = self.ax.specgram(data, Fs=sample_rate, NFFT=1024,
                                                                 cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im, ax=self.ax)
        cbar.set_label('Intensity (dB)')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Frequency (Hz)')
        self.ax.set_title('Spectrogram')
        self.canvas.draw()

    def update_rt60_label(self, spectrum, freqs, t):

        target_frequency, rt60 = self.controller.calculate_rt60_value(spectrum, freqs, t)

        self.rt60_label.config(text=f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)}'
                                    f' seconds', fg='black')
