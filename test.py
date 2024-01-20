from scipy import fft
import numpy as np
import pydub
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys


def frequency_spectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = np.arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft.fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    return frqarr, abs(x)

def convert_to_bins(freq, x, no_bins=8):
    """
    Takes the fft values and reduces the number of bars by averaging
    :param freq: the audio frequency
    :param x: the audio frequency level
    :param no_bins: the number of bars to convert to
    :returns: np.arrays containing audio freq and levels with the desired bar count
    """
    chunck = (freq.size // no_bins) + 1 # The chunck size to average

    freq_bins = np.zeros(no_bins)
    x_bins = np.zeros(no_bins)

    start = 0
    for i, end in enumerate(range(start, freq.size, chunck)):
        # Averaging levels of size chunck
        x_bins[i] = min(x[start:end].mean(), 495) # Setting 495 as the maximum level
        freq_bins[i] = freq[start:end].mean()
        start = end
    
    return freq_bins, x_bins


# Opening audio file
audio = pydub.AudioSegment.from_mp3("./test.mp3")


# Coverting audio from pydub in to samples (waveform)
waves = audio[0:42].get_array_of_samples()
freq, x = frequency_spectrum(waves, 32) # Computing frequencies and levels
freq, x = convert_to_bins(freq, x, no_bins=32)

# Setting up Plot
fig, ax = plt.subplots()
fig.set_size_inches(19.2, 10.8) # Output at 1920x1080 Resolution

# Volume bars (Blue low, Green Mid, Red High)
bars_red = ax.bar(range(freq.size), x)
bars_green = ax.bar(range(freq.size), x)
bars_blue = ax.bar(range(freq.size), x)

# Setting Background color to black
ax.set_facecolor(((0, 0, 0)))
fig.patch.set_facecolor((0, 0, 0))

def update(frame):
    # Getting the position in audio file at current frame
    start = int((frame/60) * 1000)
    end = start + 17 # 17 to get roughly 60 fps

    # Gettin frequncy and levels
    waves = audio[start:end].get_array_of_samples()
    freq, x = frequency_spectrum(waves, 32)
    freq, x = convert_to_bins(freq, x, no_bins=32)

    # Updating each volume bar height for each frequency
    for i, bar in enumerate(bars_blue):
        bar.set_height(min(x[i], 150))
        bar.set_facecolor('blue')


    for i, bar in enumerate(bars_green):
        bar.set_height(min(x[i], 350))
        bar.set_facecolor('green')

    for i, bar in enumerate(bars_red):
        bar.set_height(x[i])
        bar.set_facecolor('red')

    sys.stdout.write(f"\rAnimating...{frame/15044 * 100:.2f}%")

# Matplotlib Animator at 60fps, change save count to match length of audio file
ani = animation.FuncAnimation(fig, update, interval=16.67, blit=False, save_count=15044)

# Setting maximum y limits
plt.ylim([-0.25, 500])
plt.axis('on')

# Outputting animation at 60fps
writer = animation.FFMpegWriter(
     fps=60, bitrate=1000)
ani.save("./movie.mp4", writer=writer)
print("\rAnimating...Done")