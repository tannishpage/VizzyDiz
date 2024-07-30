import pygame
from scipy import fft
import numpy as np
import pydub
import sys

# Initializing pygame
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.draw.circle(screen, (255, 255, 255), ((300, 300)), 75)
pygame.display.flip()

audio = pydub.AudioSegment.from_mp3("./test3.mp3")

running = True
x = 0
y = 0
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    pygame.display.flip()

    
    pygame.time.wait(17)

pygame.quit()