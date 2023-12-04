from model import Model
from view import View
from controller import Controller
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('S.P.I.D.A.M.')

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # Creates a controller
        controller = Controller(model, view)

        # Sets the controller to a view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()

"""
def openFile():
    filepath = filedialog.askopenfilename(title="Please select a .wav file.",
                                          filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
    return filepath


# Create the main Tkinter window
root = Tk()

# Call the openFile function to get the file path
wav_fname = openFile()

if wav_fname:
    # Read the WAV file using soundfile
    data, sample_rate = sf.read(wav_fname)

    # Check if the WAV file has more than one channel
    if len(data.shape) > 1:
        # If there are multiple channels, take the mean across channels to get mono audio
        mono_data = np.mean(data, axis=1)
        print("Multi-channel detected. Converting to mono.")

    # If WAV file only has one channel
    else:
        mono_data = data
        print("Single-channel WAV file detected.")

    duration = len(mono_data) / sample_rate
    print(f"Duration: {duration:.2f} seconds")

    plt.plot(mono_data)
    plt.title('Audio Signal')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.savefig('audio_plot.png')
    plt.show()

    print(f"Sample rate: {sample_rate}, Data shape: {mono_data.shape}")

# Start the Tkinter event loop
root.mainloop()
"""
