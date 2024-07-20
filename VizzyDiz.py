from scipy import fft
import numpy as np
import pydub
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

# Generic Visualizer Parent Class, will be inherited by 
# child classes that do more specific visualizing.
class AudioVisualizer:

    def __init__(self, audio_file, sampling_frequency, no_bins=8):
        self._audio_file = audio_file
        self._sampling_frequncy = sampling_frequency
        self._no_bins = no_bins

    def frequency_spectrum(self, x, sf):
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

    def discretize(self, freq, x, no_bins=8):
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

    def update(self, frame):
        pass

    def _load_audio(self):
        self._audio = pydub.AudioSegment.from_mp3(self._audio_file)

    def setup_annimation(self):
        pass

    def setup_plot(self):
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(19.2, 10.8) # Output at 1920x1080 Resolution
    
    def setup_visualizer(self):
        pass



class BarVisualizer(AudioVisualizer):
    pass

class CircularScatterVisualizer(AudioVisualizer):
    pass