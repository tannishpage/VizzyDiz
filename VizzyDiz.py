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
        pass

    def convert_to_bins(self, freq, x, no_bins=8):
        pass

    def update(self, frame):
        pass

    def _load_audio(self):
        pass

    def setup_annimation(self):
        pass

    def setup_plot(self):
        pass

class BarVisualizer(AudioVisualizer):
    pass

class CircularScatterVisualizer(AudioVisualizer):
    pass