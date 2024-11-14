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
import os
import platform
from pathlib import Path

# Initializing pygame

pydub.AudioSegment.ffmpeg = "./ffmpeg.exe"
pydub.AudioSegment.ffprobe = "./ffprobe.exe"

song_loc = "c:\\Users\\punug\\Music\\GPM\\GPM\\Illenium\\ASCEND\\ILLENIUM - Gorgeous.mp3"
print(song_loc)
pygame.init()
mixer.init()
mixer.music.load(song_loc)
mixer.music.set_volume(0.7)

screen = pygame.display.set_mode((1920, 1080))
pygame.draw.circle(screen, (255, 255, 255), ((960, 540)), 75)
pygame.display.flip()

audio = AudioVisualizer(song_loc, 32, 512)
audio.load_audio()
# audio = pydub.AudioSegment.from_mp3("./test3.mp3")

running = True
x = 0
y = 0

def circle_coords(x, r, half=-1):
    return -1 * half * math.sqrt(r**2 - (x - CIRCLE_CENTER[0])**2) + CIRCLE_CENTER[1]

CIRCLE_CENTER = (960, 540)
RADIUS = 128

x_coords = range(CIRCLE_CENTER[0] - RADIUS, CIRCLE_CENTER[0] + RADIUS + 1)
y_coords_bottom = [circle_coords(x, RADIUS) for x in x_coords]
y_coords_top = [circle_coords(x, RADIUS, half=1) for x in x_coords]
print(len(y_coords_bottom), len(y_coords_top))

circle_locs_bottom = [(x, y) for x, y in zip(x_coords, y_coords_bottom)]
circle_locs_top = [(x, y) for x, y in zip(x_coords, y_coords_top)]

def update(frame, screen, audio, start, end):
    # start = int((frame/60) * 1000) 
    # end = start + length # 17 to get roughly 60 fps

    waves = audio._audio[start:end].get_array_of_samples()
    if len(waves) == 0:
        return
    freq, x = audio.frequency_spectrum(waves, audio._sampling_frequncy)
    freq, x = audio.discretize(freq, x, no_bins=audio._no_bins)
    # print(start/1000, frame)

    # print(freq)
    # Have pre-made geometries that you deform based on freq_dist
    # For a simple one, assign a circle for each freq, and change size based on freq value
    # semi_circle = 
    threshold = 10
    locs_top = []
    locs_bottom = []
    
    for i, x_val in enumerate(x[0:257]):
        #print((x_val % 255), type(x_val), str(x_val) == 'nan', x_val)
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            continue
        locs_bottom.append((x_coords[i], y_coords_bottom[i] + x_val ))

    for i, x_val in enumerate(x[257:], 257):
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            continue
        locs_top.append((x_coords[i - 257], y_coords_top[i - 257] - x_val))
        
    pygame.draw.lines(screen, (255, 255, 255), False, locs_top, 5)
    pygame.draw.lines(screen, (255, 255, 255), False, locs_bottom, 5)


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
    # pygame.draw.lines(screen, (255, 255, 255), False, circle_locs_top, 5)
    # pygame.draw.lines(screen, (255, 255, 255), False, circle_locs_bottom, 5)
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