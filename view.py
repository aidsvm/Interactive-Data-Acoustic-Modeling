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
        # Initialize the GUI components
        super().__init__(parent)

        # Create and place widgets
        # Load Button
        self.load_button = tk.Button(self, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=1, column=1, pady=10)

        self.graph_functions = [
            self.plot_waveform,
            # self.plot_combined_rt60,
            self.plot_low_rt60,
            self.plot_mid_rt60,
            self.plot_high_rt60,
            self.plot_spectrogram
        ]
        self.graph_index = 0

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.canvas.draw()

        # Button to change graph
        self.change_graph_button = tk.Button(self, text="Switch Graph", command=self.change_graph)
        self.change_graph_button.grid(row=2, column=1, pady=10)

        # Button to combine frequencies
        self.combine_button = tk.Button(self, text="Combine Frequencies", command=self.combine_frequencies)
        self.combine_button.grid(row=3, column=1, pady=10)

        # Filename Label
        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=10, column=1)

        # Display RT60
        self.rt60_label = tk.Label(self, text="")
        self.rt60_label.grid(row=10, column=1, pady=10)

        # # RT60 Plots for Low, Medium, High Frequencies
        # self.rt60_canvas = tk.Canvas(self, width=400, height=200)
        # self.rt60_canvas.grid(row=15, column=1, pady=10)

        # # Waveform Plot
        # self.waveform_canvas = tk.Canvas(self, width=400, height=200)
        # self.waveform_canvas.grid(row=15, column=1, pady=10)

        # # Graphs the waveform to the GUI
        # self.fig_waveform = Figure(figsize=(7, 5), dpi=100)
        # self.ax_waveform = self.fig_waveform.add_subplot(111)
        # self.canvas_waveform = FigureCanvasTkAgg(self.fig_waveform, master=self.waveform_canvas)
        # self.canvas_waveform.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        # self.rt60_fig_waveform = Figure(figsize=(7, 5), dpi=100)
        # self.rt60_ax_waveform = self.rt60_fig_waveform.add_subplot(111)
        # self.rt60_canvas_waveform = FigureCanvasTkAgg(self.rt60_fig_waveform, master=self.rt60_canvas)
        # self.rt60_canvas_waveform.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Highest freq
        self.highest_res_freq_label = tk.Label(self, text="")
        self.highest_res_freq_label.grid(row=17, column=1, pady=10)

        # Total time of audio file
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=18, column=1, pady=5)

        # # Additional Plots
        # self.additional_canvas = tk.Canvas(self, width=400, height=200)
        # self.additional_canvas.grid(row=19, column=1, pady=10)

        # set the controller
        self.controller = None

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
        # Clear the current graph
        self.ax.clear()

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

    def update_rt60_label(self, rt60_value):
        # Update RT60 label
        self.rt60_label.config(text=f"RT60 Value: {rt60_value} seconds")

    def display_highest_freq(self, highest_res_freq):
        # Display the highest resonance frequency on the GUI
        self.highest_res_freq_label.config(text=f"Highest Resonance Frequency: {highest_res_freq:.2f} Hz")

    # def update_waveform_plot(self, waveform_data, length):
    #     # Update Waveform Plot
    #     self.plot_waveform(waveform_data, length)

    # def update_additional_plot(self, additional_data, time):
    #     # Update Additional Plot
    #     self.plot_additional(additional_data, time)

    # def update_spectrogram(self, file_path):
    #     # Update RT60 Plot
    #     self.plot_spectrogram(file_path)

    # def plot_frequency_ranges(self, low_freq, medium_freq, high_freq):
    #     # Plot frequency ranges on the GUI
    #     self.additional_canvas.delete("all")
    #
    #     # Placeholder lines for low, medium, and high frequency ranges
    #     self.additional_canvas.create_line(0, 50, 400, 50, fill="blue")  # Low frequencies
    #     self.additional_canvas.create_line(0, 100, 400, 100, fill="orange")  # Medium frequencies
    #     self.additional_canvas.create_line(0, 150, 400, 150, fill="red")  # High frequencies
    #
    #     # Optionally, you can add labels for better clarity
    #     self.additional_canvas.create_text(200, 30, text="Low Frequencies", fill="blue")
    #     self.additional_canvas.create_text(200, 80, text="Medium Frequencies", fill="orange")
    #     self.additional_canvas.create_text(200, 130, text="High Frequencies", fill="red")

    def plot_waveform(self):
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
        filepath = self.controller.model.file_path

        fs, signal = wavfile.read(filepath)

        # Low RT60
        low_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'low')
        time_axis_low = np.arange(0, len(signal)) / fs
        if len(low_rt60_db) != len(time_axis_low):
            low_rt60_db = np.interp(time_axis_low, np.linspace(0, 1, len(low_rt60_db)), low_rt60_db)
        amplitude_low = np.exp(-low_rt60_db / 20 * time_axis_low)

        # Mid RT60
        mid_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'mid')
        time_axis_mid = np.arange(0, len(signal)) / fs
        if len(mid_rt60_db) != len(time_axis_mid):
            mid_rt60_db = np.interp(time_axis_mid, np.linspace(0, 1, len(mid_rt60_db)), mid_rt60_db)
        amplitude_mid = np.exp(-mid_rt60_db / 20 * time_axis_mid)

        # High RT60
        high_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'high')
        time_axis_high = np.arange(0, len(signal)) / fs
        if len(high_rt60_db) != len(time_axis_high):
            high_rt60_db = np.interp(time_axis_high, np.linspace(0, 1, len(high_rt60_db)), high_rt60_db)
        amplitude_high = np.exp(-high_rt60_db / 20 * time_axis_high)

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

        # Redraw the canvas with the new graph
        self.canvas.draw()

    def plot_low_rt60(self):
        filepath = self.controller.model.file_path

        fs, signal = wavfile.read(filepath)

        low_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'low')

        time_axis = np.arange(0, len(signal)) / fs

        if len(low_rt60_db) != len(time_axis):
            low_rt60_db = np.interp(time_axis, np.linspace(0, 1, len(low_rt60_db)), low_rt60_db)

        amplitude = np.exp(-low_rt60_db / 20 * time_axis)

        threshold = -60
        decay_point = np.argmax(amplitude <= threshold)
        self.ax.plot(time_axis, 20 * np.log10(amplitude), label='Decay Curve')

        self.ax.scatter(time_axis[decay_point], 20 * np.log10(amplitude[decay_point]), color='red',
                        label='60 dB Decay Point')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('Low Reverberation Time Calculation')
        self.ax.legend()

    def plot_mid_rt60(self):
        filepath = self.controller.model.file_path

        fs, signal = wavfile.read(filepath)

        mid_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'mid')

        time_axis = np.arange(0, len(signal)) / fs

        if len(mid_rt60_db) != len(time_axis):
            mid_rt60_db = np.interp(time_axis, np.linspace(0, 1, len(mid_rt60_db)), mid_rt60_db)

        amplitude = np.exp(-mid_rt60_db / 20 * time_axis)

        threshold = -60
        decay_point = np.argmax(amplitude <= threshold)
        self.ax.plot(time_axis, 20 * np.log10(amplitude), label='Decay Curve')

        self.ax.scatter(time_axis[decay_point], 20 * np.log10(amplitude[decay_point]), color='red',
                        label='60 dB Decay Point')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (dB)')
        self.ax.set_title('Mid Reverberation Time Calculation')
        self.ax.legend()

    def plot_high_rt60(self):
        filepath = self.controller.model.file_path

        fs, signal = wavfile.read(filepath)

        high_rt60_db = self.controller.compute_rt60_for_frequencies(filepath, 'high')

        time_axis = np.arange(0, len(signal)) / fs

        if len(high_rt60_db) != len(time_axis):
            high_rt60_db = np.interp(time_axis, np.linspace(0, 1, len(high_rt60_db)), high_rt60_db)

        amplitude = np.exp(-high_rt60_db / 20 * time_axis)

        threshold = -60
        decay_point = np.argmax(amplitude <= threshold)
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
        spectrum, freqs, t, im = self.ax.specgram(data, Fs=sample_rate, NFFT=1024,
                                                  cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im, ax=self.ax)
        cbar.set_label('Intensity (dB)')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Frequency (Hz)')
        self.ax.set_title('Spectrogram')
        self.canvas.draw()

    # def plot_additional(self, data, canvas):
    #     # Plot additional data on the GUI
    #     canvas.delete("all")
    #     canvas.create_line(0, 100, 400, 100, fill="green")  # Placeholder line for additional plot
