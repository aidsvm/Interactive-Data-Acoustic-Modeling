import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create and place widgets
        # Load Button
        self.load_button = tk.Button(self, text="Load Audio", command=self.load_sample)
        self.load_button.pack(pady=10)

        # Filename Label
        self.filename_label = tk.Label(self, text="File: No file selected")
        self.filename_label.pack(pady=5)

        # Display RT60
        self.rt60_label = tk.Label(self, text="RT60 Value:")
        self.rt60_label.pack(pady=5)

        # Waveform Plot
        self.waveform_canvas = tk.Canvas(self, width=400, height=200)
        self.waveform_canvas.pack(pady=10)

        # Additional Plots
        self.additional_canvas = tk.Canvas(self, width=400, height=200)
        self.additional_canvas.pack(pady=10)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def load_sample(self):
        # Open file dialog for selecting audio file
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))

        if file_path:
            # Notify the Controller about the user's action
            self.controller.load_sample(file_path)

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
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="blue")  # Placeholder line for waveform

    def plot_additional(self, data, canvas):
        canvas.delete("all")
        canvas.create_line(0, 100, 400, 100, fill="green")  # Placeholder line for additional plot
