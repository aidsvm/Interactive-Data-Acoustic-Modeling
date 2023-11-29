import numpy as np
from scipy.io import wavfile
from tkinter import *
from tkinter import filedialog
import soundfile as sf
import matplotlib.pyplot as plt


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
