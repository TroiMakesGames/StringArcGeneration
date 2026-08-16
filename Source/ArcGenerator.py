import pygame

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

def arc_point(p1, p2, focusLength, t, flip=False):

    #check t
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be between 0 and 1")

    x1, y1 = p1
    x2, y2 = p2

    #vecto p1-p2
    dx = x2 - x1
    dy = y2 - y1

    length = math.hypot(dx, dy)

    #check distance
    if length == 0:
        raise ValueError("p1 and p2 must be different points")

    #get normal vector + circle center
    #midpoint
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    #normalized
    nx = -dy / length
    ny = dx / length
    #multiplied by focusLength
    cx = mx + nx * focusLength
    cy = my + ny * focusLength

    #get radius
    radius = math.hypot(x1 - cx, y1 - cy)

    #get angles from center to each point
    angle1 = math.atan2(y1 - cy, x1 - cx)
    angle2 = math.atan2(y2 - cy, x2 - cx)

    #get diff for proper interpolation
    delta = angle2 - angle1

    #normalize to pi for circular nature
    delta = (delta + math.pi) % (2 * math.pi) - math.pi

    #select longer arc instead
    if flip:
        if delta > 0:
            delta -= 2 * math.pi
        else:
            delta += 2 * math.pi

    #interpolate angle
    angle = angle1 + delta * t

    #convert to polar coords
    x = cx + math.cos(angle) * radius
    y = cy + math.sin(angle) * radius

    return (x, y)

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
        arcPoints.append(arc_point(p1, p2, -500, i/250, True))

    for arcPoint in arcPoints:
        pygame.draw.circle(screen, (100, 100, 100), arcPoint, 2)

    arcPoints = []
    for i in range(30):
            arcPoints.append(arc_point(p1, p2, 500, i/30))
    
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
