import pygame
from pygame import mixer
from scipy import fft
import numpy as np
import random
import pydub
import sys
import time
import math
from VizzyDiz import AudioVisualizer

# Initializing pygame

song_loc = "/Users/aravind/Nextcloud/Music/GPM/Illenium/ASCEND/ILLENIUM - Gorgeous.mp3"

pygame.init()
mixer.init()
mixer.music.load(song_loc)
mixer.music.set_volume(0.7)

screen = pygame.display.set_mode((1920, 1080))
pygame.draw.circle(screen, (255, 255, 255), ((300, 300)), 75)
pygame.display.flip()


audio = AudioVisualizer(song_loc, 2, 64)
audio.load_audio()
# audio = pydub.AudioSegment.from_mp3("./test3.mp3")

running = True
x = 0
y = 0

def update(frame, screen, audio, start, end):
    # start = int((frame/60) * 1000)
    # end = start + length # 17 to get roughly 60 fps

    waves = audio._audio[start:end].get_array_of_samples()
    freq, x = audio.frequency_spectrum(waves, audio._sampling_frequncy)
    freq, x = audio.discretize(freq, x, no_bins=audio._no_bins)
    # print(start/1000, frame)

    # print(freq)
    # Have pre-made geometries that you deform based on freq_dist
    # For a simple one, assign a circle for each freq, and change size based on freq value
    threshold = 10

    for i, x_val in enumerate(sorted(x)):
        #print((x_val % 255), type(x_val), str(x_val) == 'nan', x_val)
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            continue
        pygame.draw.circle(screen, (((x_val*1.33*random.uniform(5, 5.1)) % 255)//1, ((x_val*0.5*random.uniform(5, 5.1)) % 255)//1, ((x_val*0.78*random.uniform(5, 5.1)) % 255)//1 ), ((i*15 + 100, 1080 - (x_val+300) )), min( x_val, 100)+3)


frame = 0
t_dif = 0.017
dt = 17
mixer.music.play()
start = 0
end = start + dt
clock = pygame.time.Clock()
while running:
    
    start_t = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update(frame, screen, audio, start, end)
    pygame.display.flip()

    frame += 1
    # if frame % 2 == 0:
    #     pygame.time.wait(9)
    # else:
    #     pygame.time.wait(10)
    screen.fill((0,0,0))
    end_t = time.time()
    t_dif = end_t - start_t
    dt = clock.tick(60)
    start = end
    end = start + dt
    # print(1/(t_dif), t_dif, dt)
    # pygame.display.flip()

    
    # pygame.time.wait(17)
    # pygame.draw.circle(screen, (255, 255, 255), ((300, 300)), 75)
    # pygame.display.flip()

pygame.quit()