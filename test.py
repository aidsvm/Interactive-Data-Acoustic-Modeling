import numpy as np
import matplotlib.pyplot as plt


def rt60_curve(decay_rate, time_interval):
    """
    Generate an RT60 curve.

    Parameters:
    - decay_rate: The rate of decay (e.g., 60 dB)
    - time_interval: The time interval for the decay curve

    Returns:
    - time: Time values
    - sound_level: Sound level values corresponding to the time values
    """
    time = np.arange(0, 5 * time_interval, time_interval)  # Adjust the time range as needed
    sound_level = 0 - decay_rate * time / 60.0
    return time, sound_level


def plot_rt60_graph():
    decay_rate = 60  # RT60 value in dB
    time_interval = 0.1  # Adjust the time interval as needed

    time, sound_level = rt60_curve(decay_rate, time_interval)

    plt.plot(time, sound_level, label=f'RT60 = {decay_rate} dB')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Sound Level (dB)')
    plt.title('RT60 Decay Curve')
    plt.axhline(y=-60, color='r', linestyle='--', label='-60 dB Reference')  # Horizontal line at -60 dB
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_rt60_graph()
