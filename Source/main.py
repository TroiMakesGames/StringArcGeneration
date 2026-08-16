import pygame

import ArcGenerator

import math
import random

#initialize pygame window
pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('<Title>')

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, font_size):
    font = pygame.font.SysFont(None, font_size)
    fps = round(clock.get_fps(), 1)
    fps_text = font.render(f"{fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

#CLASS DEFINITION -----------------------------------------------------------------------------------------------------------------------------------------

#FUNCTION DEFINITION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#VARIABLE INITIALIZATION -----------------------------------------------------------------------------------------------------------------------------------------

#get initial ticks
prevT = pygame.time.get_ticks()

#WHILE LOOP - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

running = True
while running:

    #update delta time
    currT = pygame.time.get_ticks()
    dTms = currT - prevT
    dTs = dTms / 1000.0

    #fill screen
    screen.fill((20, 20, 20))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #use example
    p1 = (200, 250)
    p2 = (600, 350)

    arcPoints = []
    for i in range(250):
        arcPoints.append(ArcGenerator.arc_point(p1, p2, -500, i/250, True))

    for arcPoint in arcPoints:
        pygame.draw.circle(screen, (100, 100, 100), arcPoint, 2)

    arcPoints = []
    for i in range(30):
            arcPoints.append(ArcGenerator.arc_point(p1, p2, 500, i/30))
    
    for arcPoint in arcPoints:
        pygame.draw.circle(screen, (255, 255, 255), arcPoint, 2)

    pygame.draw.circle(screen, (255, 0, 0), p1, 5)
    pygame.draw.circle(screen, (255), p2, 5)

    # Update the display (buffer flip)
    displayFPS(screen, 25)
    pygame.display.flip()
    clock.tick(60)

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
