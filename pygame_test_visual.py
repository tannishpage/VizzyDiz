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
# time.sleep(5)
# Initializing pygame

pydub.AudioSegment.ffmpeg = "./ffmpeg.exe"
pydub.AudioSegment.ffprobe = "./ffprobe.exe"

song_loc = "c:\\Users\\punug\\Music\\GPM\\GPM\\Linkin Park\\Minutes to Midnight\\Linkin Park - What I've Done.mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\Illenium\\Ashes\\Illenium - Reverie (feat. King Deco).mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\Illenium\\ASCEND\\ILLENIUM - Gorgeous.mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\CHVRCHES\\The Bones Of What You Believe\\01 The Mother We Share.mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\JVNA\\Living in Hell\\JVNA - Living in Hell.mp3" #"c:\\Users\\punug\\Music\\GPM\\GPM\\Illenium\\ILLENIUM\\Illenium - 05. Lifeline.mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\Nicky Romero vs. Krewella\\Legacy (Remixes)\\Nicky Romero - Legacy (Vicetone Remix).mp3" # "c:\\Users\\punug\\Music\\GPM\\GPM\\Linkin Park\\Minutes to Midnight\\Linkin Park - What I've Done.mp3"
print(song_loc)
pygame.init()
mixer.init()
mixer.music.load(song_loc)
mixer.music.set_volume(0.7)


screen_height = 1440
screen_width = 2560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.draw.circle(screen, (255, 255, 255), ((960, 540)), 75)
pygame.display.flip()

no_bins = 1024

audio = AudioVisualizer(song_loc, 32, no_bins)
audio.load_audio()
# audio = pydub.AudioSegment.from_mp3("./test3.mp3")

running = True
x = 0
y = 0

def circle_coords(x, r, half=-1):
    return -1 * half * math.sqrt(r**2 - (x - CIRCLE_CENTER[0])**2) + CIRCLE_CENTER[1]

CIRCLE_CENTER = (screen_width//2, screen_height//2)
RADIUS = 512

x_coords = range(CIRCLE_CENTER[0] - RADIUS, CIRCLE_CENTER[0] + RADIUS + (RADIUS*2)//(no_bins//2), (RADIUS*2)//(no_bins//2))
y_coords_bottom = [circle_coords(x, RADIUS) for x in x_coords]
y_coords_top = [circle_coords(x, RADIUS, half=1) for x in x_coords]
print(len(y_coords_bottom), len(y_coords_top))

circle_locs_bottom = [(x, y) for x, y in zip(x_coords, y_coords_bottom)]
circle_locs_top = [(x, y) for x, y in zip(x_coords, y_coords_top)]

def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def update(frame, screen, audio, start, end):
    # start = int((frame/60) * 1000) 
    # end = start + length # 17 to get roughly 60 fps

    waves = audio._audio[start:end].get_array_of_samples()
    sample_max = max(waves)
    if len(waves) == 0:
        return
    freq, x = audio.frequency_spectrum(waves, audio._sampling_frequncy)
    freq, x = audio.discretize(freq, x, no_bins=audio._no_bins)
    # print(start/1000, frame)

    # print(freq)
    # Have pre-made geometries that you deform based on freq_dist
    # For a simple one, assign a circle for each freq, and change size based on freq value
    # semi_circle = 
    
    threshold_r = random.uniform(1, 1.05)
    locs_top_r = [circle_locs_top[0]]
    locs_bottom_r = [circle_locs_bottom[0]]
    
    threshold_b = random.uniform(1, 1.05)
    locs_top_b = [circle_locs_top[0]]
    locs_bottom_b = [circle_locs_bottom[0]]
    
    color_b = (random.randint(0, 10)*min((sample_max/SONG_MAX)+0.1, 1), random.randint(245, 255)*min((sample_max/SONG_MAX)+0.1, 1), random.randint(245, 255)*min((sample_max/SONG_MAX)+0.1, 1))
    color_r = (random.randint(245, 255)*min((sample_max/SONG_MAX)+0.1, 1), random.randint(40, 50)*min((sample_max/SONG_MAX)+0.1, 1), random.randint(203, 213)*min((sample_max/SONG_MAX)+0.1, 1))
        

    for i, x_val in enumerate(x[0:(no_bins//2)-1], 1):
        #print((x_val % 255), type(x_val), str(x_val) == 'nan', x_val)
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            continue
        
        xp = abs(x_coords[i] - CIRCLE_CENTER[0])/RADIUS
        yp = abs(y_coords_bottom[i] - CIRCLE_CENTER[1])/RADIUS
        #print(xp, yp)
        sign = sgn(x_coords[i] - CIRCLE_CENTER[0])
        randomness = random.uniform(-1*threshold_b-0.25, -1*threshold_b)
        locs_bottom_b.append((x_coords[i] + randomness*sign*x_val*xp, y_coords_bottom[i] + x_val*threshold_b*randomness*yp))

    for i, x_val in enumerate(x[(no_bins//2 + 1):-1], (no_bins//2 + 1)+1):
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            x_val = 0
        xp = abs(x_coords[i - (no_bins//2 + 1)] - CIRCLE_CENTER[0])/RADIUS
        yp = abs(y_coords_bottom[i - (no_bins//2 + 1)] - CIRCLE_CENTER[1])/RADIUS
        #print(xp, yp)
        sign = sign = sgn(x_coords[i - (no_bins//2 + 1)] - CIRCLE_CENTER[0])
        randomness = random.uniform(-1*threshold_b-0.25, -1*threshold_b)
        locs_top_b.append((x_coords[i - (no_bins//2 + 1)] + randomness*sign*x_val*xp, y_coords_top[i - (no_bins//2 + 1)] - x_val*threshold_b*randomness*yp))
        

    for i, x_val in enumerate(x[0:(no_bins//2 )-1], 1):
        #print((x_val % 255), type(x_val), str(x_val) == 'nan', x_val)
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            x_val = 0
        
        xp = abs(x_coords[i] - CIRCLE_CENTER[0])/RADIUS
        yp = abs(y_coords_bottom[i] - CIRCLE_CENTER[1])/RADIUS
        #print(xp, yp)
        sign = sgn(x_coords[i] - CIRCLE_CENTER[0])
        randomness = random.uniform(threshold_r-0.25, threshold_r)
        locs_bottom_r.append((x_coords[i] + randomness*sign*x_val*xp, y_coords_bottom[i] + x_val*threshold_r*randomness*yp))\

    for i, x_val in enumerate(x[(no_bins//2 + 1):-1], (no_bins//2 + 1)+1):
        if str(x_val) == 'nan':
            #print("LSKDJFLSKDJFLSKDJFLKJ")
            continue
        xp = abs(x_coords[i - (no_bins//2 + 1)] - CIRCLE_CENTER[0])/RADIUS
        yp = abs(y_coords_bottom[i - (no_bins//2 + 1)] - CIRCLE_CENTER[1])/RADIUS
        #print(xp, yp)
        sign = sign = sgn(x_coords[i - (no_bins//2 + 1)] - CIRCLE_CENTER[0])
        randomness = random.uniform(threshold_r-0.25, threshold_r)
        locs_top_r.append((x_coords[i - (no_bins//2 + 1)] + randomness*sign*x_val*xp, y_coords_top[i - (no_bins//2 + 1)] - x_val*threshold_r*randomness*yp))
        
    locs_top_r.append(circle_locs_top[-1])
    locs_bottom_r.append(circle_locs_bottom[-1])
    locs_top_b.append(circle_locs_top[-1])
    locs_bottom_b.append(circle_locs_bottom[-1])
    
    pygame.draw.circle(screen, (255*(sample_max/SONG_MAX), 255*(sample_max/SONG_MAX), 255*(sample_max/SONG_MAX)), ((CIRCLE_CENTER[0], CIRCLE_CENTER[1])), RADIUS*(sample_max/SONG_MAX))
        
    pygame.draw.lines(screen, color_r, False, locs_top_r, 5)
    pygame.draw.lines(screen, color_r, False, locs_bottom_r, 5)
    
    pygame.draw.lines(screen, color_b, False, locs_top_b, 5)
    pygame.draw.lines(screen, color_b, False, locs_bottom_b, 5)
    
    return (sample_max/SONG_MAX)

frame = 0
t_dif = 0.017
dt = 17
mixer.music.play()
start = 0
end = start + dt
clock = pygame.time.Clock()
SONG_MAX = max(audio._audio.get_array_of_samples())
while running:
    
    start_t = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vol = update(frame, screen, audio, start, end)
    # pygame.draw.lines(screen, (255, 255, 255), False, circle_locs_top, 5)
    # pygame.draw.lines(screen, (255, 255, 255), False, circle_locs_bottom, 5)
    pygame.display.flip()

    frame += 1
    # if frame % 2 == 0:
    #     pygame.time.wait(9)
    # else:
    #     pygame.time.wait(10)
    screen.fill((0, 0, 0))
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