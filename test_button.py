import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class GraphSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Switcher")

        self.graph_functions = [
            self.waveform,
            self.combined_rt60,
            self.low_rt60,
            self.mid_rt60,
            self.high_rt60,
            self.spectrogram
        ]
        self.graph_index = 0

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

        button = tk.Button(root, text="Switch Graph", command=self.change_graph)
        button.pack()

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

    def waveform(self):
        # Replace with your waveform plotting logic
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.ax.set_title("Waveform")

    def combined_rt60(self):
        # Replace with your combined_rt60 plotting logic
        # Example data
        categories = ['Category A', 'Category B', 'Category C']
        values = [3, 5, 2]
        self.ax.bar(categories, values)
        self.ax.set_title("Combined RT60")

    def low_rt60(self):
        # Replace with your low_rt60 plotting logic
        # Example data
        labels = ['Label A', 'Label B', 'Label C']
        sizes = [15, 30, 45]
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax.set_title("Low RT60")

    def mid_rt60(self):
        # Replace with your mid_rt60 plotting logic
        # Example data
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(0, 0.1, 100)
        self.ax.plot(x, y)
        self.ax.set_title("Mid RT60")

    def high_rt60(self):
        # Replace with your high_rt60 plotting logic
        # Example data
        x = np.linspace(0, 5, 100)
        y = np.exp(x)
        self.ax.plot(x, y)
        self.ax.set_title("High RT60")

    def spectrogram(self):
        # Replace with your spectrogram plotting logic
        # Example data
        data = np.random.random((10, 10))
        self.ax.imshow(data, cmap='viridis', aspect='auto', origin='lower')
        self.ax.set_title("Spectrogram")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphSwitcherApp(root)
    root.mainloop()
