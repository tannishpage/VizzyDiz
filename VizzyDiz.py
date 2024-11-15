from scipy import fft
import numpy as np
import pydub
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import pygame
from pygame import mixer

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

        # frqarr = frqarr[range(n // 2)]  # one side frequency range

        x = fft.fft(x) / n  # fft computing and normalization
        # x = x[range(n // 2)]
        # x = x / x.max()

        return frqarr, abs(x)

    def discretize(self, freq, x, no_bins=8):
        """
        Takes the fft values and reduces the number of bars by averaging
        :param freq: the audio frequency
        :param x: the audio frequency level
        :param no_bins: the number of bars to convert to
        :returns: np.arrays containing audio freq and levels with the desired bar count
        """
        chunck = freq.size + 1 - no_bins  # (freq.size // no_bins) + 1 # The chunck size to average
        # print(freq.size, chunck)

        freq_bins = np.zeros(no_bins)
        x_bins = np.zeros(no_bins)

        start = 0
        end = start + chunck
        i = 0
        # for i, end in enumerate(range(start, freq.size, chunck)):
        #     # Averaging levels of size chunck
        #     x_bins[i] = min(x[start:end].mean(), 300) # Setting 495 as the maximum level
        #     freq_bins[i] = freq[start:end].mean()
        #     start = end
        
        while end != freq.size:
            x_bins[i] = min(x[start:end].mean(), 495)
            start += 1
            end = start + chunck
            i += 1
        return freq_bins, x_bins

    def load_audio(self):
        self._audio = pydub.AudioSegment.from_mp3(self._audio_file)


class BarVisualizer(AudioVisualizer):
    def __init__(self, audio_file, sampling_frequency, number_of_bar_sets=3, bar_colors=((0, 0, 1), (0, 1, 0), (1, 0, 0)), bar_set_max_heights=(250, 450, 1000), no_bins=8, fig_height=19.2, fig_width=10.8):
        super().__init__(audio_file, sampling_frequency, no_bins)
        
        self.number_of_bar_sets = number_of_bar_sets
        self.bar_colors = bar_colors

        self.setup_plot()
        self.load_audio()

    def setup_plot(self):
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(19.2, 10.8) # Output at 1920x1080 Resolution
        self.ax.set_facecolor(((0, 0, 0)))
        self.fig.patch.set_facecolor((0, 0, 0))

        self.bar_sets = [None for x in range(self.number_of_bar_sets)]

        for bar_set in range(self.number_of_bar_sets):
            self.bar_sets[bar_set] = self.ax.bar(range(self._no_bins), range(self._no_bins))


    def update(self, frame):
        start = int((frame/60) * 1000)
        end = start + 17 # 17 to get roughly 60 fps

        # Gettin frequncy and levels
        waves = self._audio[start:end].get_array_of_samples()
        freq, x = self.frequency_spectrum(waves, self._sampling_frequncy)
        freq, x = self.discretize(freq, x, no_bins=self._no_bins)

        # Updating each volume bar height for each frequency
        for bar_set_num, bar_set in enumerate(self.bar_sets):
            for i, bar in enumerate(bar_set):
                bar.set_height(min(x[i], 250))
                bar.set_facecolor(self.bar_colors[bar_set_num])

        sys.stdout.write(f"\rAnimating...{frame/18500 * 100:.2f}%")


class CircularScatterVisualizer(AudioVisualizer):
    pass

class PyGameTestVisualizer(AudioVisualizer):
    def __init__(self, audio_file, sampling_frequency, no_bins=8, screen_resolution=(1280, 720)):
        super().__init__(audio_file, sampling_frequency, no_bins)
        pygame.init()
        
        mixer.init()
        mixer.music.load(song_loc)
        mixer.music.set_volume(0.7)

        self.screen = pygame.display.set_mode(())
        self.clock = pygame.time.Clock()

        self.setup_plot()
        self.load_audio()

    def update(self, screen, start, end):
        # How to draw each frame
        waves = self._audio[start:end].get_array_of_samples()
        freq, x = self.frequency_spectrum(waves, self._sampling_frequncy)
        freq, x = self.discretize(freq, x, no_bins=self._no_bins)

        for i, x_val in enumerate(x):
            if str(x_val) == 'nan':
                continue
            pygame.draw.circle(screen, (((x_val*1.33*random.uniform(0, 5)) % 255)//1, ((x_val*0.5*random.uniform(0, 5)) % 255)//1, ((x_val*0.78*random.uniform(0, 5)) % 255)//1 ), ((i*15 + 100, 1080 - (x_val+300) )), min( x_val, 50)+3, width=10)

    def main_loop():
        # The main loop that calls update
        pass

def main():
    visualizer = BarVisualizer("./test.mp3", 32, no_bins=64)
    ani = animation.FuncAnimation(visualizer.fig, visualizer.update, interval=16.67, blit=False, save_count=18500)
    # Setting maximum y limits
    plt.ylim([-0.25, 500])
    plt.axis('on')

    # Outputting animation at 60fps
    writer = animation.FFMpegWriter(
        fps=60, bitrate=1000)
    ani.save("./movie3.mp4", writer=writer)
    print("\rAnimating...Done")

if __name__ == "__main__":
    main()