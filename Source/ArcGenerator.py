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
    """
    Return a point on the circular arc from p1 to p2.

    Parameters
    ----------
    p1, p2 : tuple[float, float]
        The two endpoints of the arc.

    focusLength : float
        Distance from the midpoint of p1-p2 to the circle center,
        measured along the perpendicular to the line.

    t : float
        Interpolation value from 0.0 to 1.0.
        0.0 -> p1
        0.5 -> midpoint of the selected arc
        1.0 -> p2

    flip : bool
        False -> shorter arc
        True  -> longer arc

    Returns
    -------
    tuple[float, float]
        The interpolated point on the arc.
    """

    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be between 0 and 1")

    x1, y1 = p1
    x2, y2 = p2

    # Vector from p1 to p2
    dx = x2 - x1
    dy = y2 - y1

    length = math.hypot(dx, dy)

    if length == 0:
        raise ValueError("p1 and p2 must be different points")

    # Midpoint of the chord
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    # Normalized perpendicular vector
    nx = -dy / length
    ny = dx / length

    # Circle center
    cx = mx + nx * focusLength
    cy = my + ny * focusLength

    # Radius
    radius = math.hypot(x1 - cx, y1 - cy)

    # Angles from center to endpoints
    angle1 = math.atan2(y1 - cy, x1 - cx)
    angle2 = math.atan2(y2 - cy, x2 - cx)

    # Difference between the angles
    delta = angle2 - angle1

    # Normalize to [-pi, pi]
    delta = (delta + math.pi) % (2 * math.pi) - math.pi

    # Select the long arc instead of the short arc
    if flip:
        if delta > 0:
            delta -= 2 * math.pi
        else:
            delta += 2 * math.pi

    # Interpolate the angle
    angle = angle1 + delta * t

    # Convert polar coordinates back to Cartesian
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

        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass"""

    """keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pass"""

    p1 = (200, 250)
    p2 = (600, 350)

    arcPoints = []
    for i in range(250):
        arcPoints.append(arc_point(p1, p2, -500, i/250, True))

    for arcPoint in arcPoints:
        pygame.draw.circle(screen, (155, 155, 155), arcPoint, 2)

    arcPoints = []
    for i in range(250):
            arcPoints.append(arc_point(p1, p2, 500, i/250))
    
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
