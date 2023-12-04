import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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

        # Waveform Plot
        self.waveform_canvas = tk.Canvas(self, width=400, height=200, )
        self.waveform_canvas.grid(row=15, column=1, pady=10)

        self.fig_waveform = Figure(figsize=(7, 5), dpi=100)
        self.ax_waveform = self.fig_waveform.add_subplot(111)
        self.canvas_waveform = FigureCanvasTkAgg(self.fig_waveform, master=self.waveform_canvas)
        self.canvas_waveform.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


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

    def update_waveform_plot(self, waveform_data):
        # Update Waveform Plot
        self.plot_waveform(waveform_data, self.waveform_canvas)

    def update_additional_plot(self, additional_data):
        # Update Additional Plot
        self.plot_additional(additional_data, self.additional_canvas)

    def plot_waveform(self, data, canvas):
        self.ax_waveform.clear()
        self.ax_waveform.plot(data)
        self.ax_waveform.set_title('Audio Signal')
        self.ax_waveform.set_xlabel('Sample Index')
        self.ax_waveform.set_ylabel('Amplitude')

        # Redraw the canvas
        self.canvas_waveform.draw()

    def plot_additional(self, data, canvas):
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="green")  # Placeholder line for additional plot
