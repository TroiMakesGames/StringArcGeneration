import pygame

from ArcGenerator import circularArc

import math
import numpy as np
import random

#initialize pygame window
pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('String Arc Generation')

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, font_size):
    font = pygame.font.SysFont(None, font_size)
    fps = round(clock.get_fps(), 1)
    fps_text = font.render(f"{fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

#CLASS DEFINITION -----------------------------------------------------------------------------------------------------------------------------------------

class Circle():
    def __init__(self, center, radius):
        circles.append(self)

        self.center = center
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, (100, 100, 100), self.center, self.radius, 2)
        pygame.draw.circle(screen, (100, 100, 100), self.center, 2)

class Hand():
    def __init__(self):
        self.isDown = False
        self.mouseStartPos = None
        self.lastSegmentStart = None

        self.points = []

    def recalculatePoints(self, circles):
        #clear old points
        self.points = []

        #push first point
        self.points.insert(0, self.mouseStartPos)

        #check if intersects with any circle
        self.lastSegmentStart = self.mouseStartPos
        for circle in circles:
            distanceLinePointData = distanceLinePoint(self.lastSegmentStart, pygame.mouse.get_pos(), circle.center) # -> distance, onsegment, point

            if not distanceLinePointData[1] or distanceLinePointData[0] > circle.radius:
                continue

            #check whether endpoints inside circle
            vecTo = (circle.center[0] - self.lastSegmentStart[0], circle.center[1] - self.lastSegmentStart[1])
            dist = math.sqrt(vecTo[0] * vecTo[0] + vecTo[1] * vecTo[1])
            if dist < circle.radius:
                continue

            vecTo = (circle.center[0] - pygame.mouse.get_pos()[0], circle.center[1] - pygame.mouse.get_pos()[1])
            dist = math.sqrt(vecTo[0] * vecTo[0] + vecTo[1] * vecTo[1])
            if dist < circle.radius:
                continue

            #get tangent points
            tp11, tp12 = tangentPoints(circle.center, circle.radius, self.lastSegmentStart)
            tp21, tp22 = tangentPoints(circle.center, circle.radius, pygame.mouse.get_pos())

            if tp11 == False or tp12 == False or tp21 == False or tp22 == False:
                break

            """
            pygame.draw.line(screen, (255, 0, 0), self.lastSegmentStart, tp11, 2)
            pygame.draw.line(screen, (255, 0, 0), tp22, pygame.mouse.get_pos(), 2)
            
            pygame.draw.line(screen, (0, 0, 255), tp21, pygame.mouse.get_pos(), 2)
            pygame.draw.line(screen, (0, 0, 255), self.lastSegmentStart, tp12, 2)
            """

            #get correct side pair
            pair = 1
            focusDirection = -1
            vecToEnd = (pygame.mouse.get_pos()[0] - self.lastSegmentStart[0], pygame.mouse.get_pos()[1] - self.lastSegmentStart[1])
            vecToCenter = (circle.center[0] - self.lastSegmentStart[0], circle.center[1] - self.lastSegmentStart[1])
            if getClockwiseAngle(vecToCenter, vecToEnd) > 180:
                pair = 2
                focusDirection = 1

            tp1, tp2 = tp11, tp22
            if pair == 1:
                tp1, tp2 = tp12, tp21

            #add first tangent point
            self.points.append(tp1)

            #get arc data
            #get focus length
            focusLength = distanceLinePoint(tp1, tp2, circle.center)[0]

            #get arc points
            interpPoints = []
            accuracy = 25
            for i in range(accuracy):
                interpPoints.append(circularArc(tp1, tp2, focusLength * focusDirection, i/accuracy, False))
            self.points = self.points + interpPoints

            #add last tangent point and update lastSegmentStart for future circles
            self.points.append(tp2)
            self.lastSegmentStart = tp2

        #append last point
        self.points.append(pygame.mouse.get_pos())

    def draw(self):
        if len(self.points) > 0:
            #draw original line
            """pygame.draw.line(screen, (100, 100, 100), self.points[0], self.points[-1], 3)"""

            #draw full line
            for i in range(len(self.points) - 1):
                pygame.draw.line(screen, (255, 255, 255), self.points[i], self.points[i + 1], 3)

#FUNCTION DEFINITION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#check for circle intersections with lines
def distanceLinePoint(a, b, p): # -> distance, onSegment, closestPoint
    ax, ay = a
    bx, by = b
    px, py = p

    abx = bx - ax
    aby = by - ay

    length_squared = abx * abx + aby * aby

    #a == b
    if length_squared == 0:
        return (math.hypot(px - ax, py - ay), False, a)

    #position of projection along ab
    t = ((px - ax) * abx + (py - ay) * aby) / length_squared

    #check onsegment
    on_segment = 0 <= t <= 1

    #clamp to segment for closest point
    t_clamped = max(0, min(1, t))

    closest_point = (ax + t_clamped * abx, ay + t_clamped * aby)

    distance = math.hypot(px - closest_point[0], py - closest_point[1])

    return distance, on_segment, closest_point

def tangentPoints(center, radius, point):
    cx, cy = center
    px, py = point

    dx = px - cx
    dy = py - cy

    d_squared = dx * dx + dy * dy

    #check if point isnide
    if d_squared < radius * radius:
        return False

    #pont is exactly on the circle - one tangent point - still return false
    if d_squared == radius * radius:
        return False

    d = math.sqrt(d_squared)

    #unit vector from center to point
    ux = dx / d
    uy = dy / d

    #distance from center to tangent points along center to point direction
    a = radius * radius / d

    #offset
    h = radius * math.sqrt(d_squared - radius * radius) / d

    #base point
    bx = cx + a * ux
    by = cy + a * uy

    #perpendicular vectoir
    px_perp = -uy
    py_perp = ux

    tangent1 = (bx + h * px_perp, by + h * py_perp)
    tangent2 = (bx - h * px_perp, by - h * py_perp)

    return tangent1, tangent2

def getClockwiseAngle(frm, to):
    #get signed angle, get absolute angle
    signedAngle = np.arctan2(frm[1], to[0]) - np.arctan2(frm[1], to[0])
    unsignedAngle = abs(signedAngle)

    #normalize unsigned between 0 and 360
    if unsignedAngle > 180:
        unsignedAngle = 360 - unsignedAngle

    #get cross product
    crossP = frm[0] * to[1] - frm[1] * to[0]

    #update to clockwise if the angle was counter clockwise
    if crossP < 0:
        unsignedAngle = 360 - unsignedAngle

    return unsignedAngle

#VARIABLE INITIALIZATION -----------------------------------------------------------------------------------------------------------------------------------------

hand = Hand()

circles = []

circle1 = Circle((screenWidth/2, screenHeight/2), 100)
circle2 = Circle((600, 250), 100)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                print(pygame.mouse.get_pos())

            #get hand inputs (mouse 0 up + down)
            if event.button == 1:
                hand.isDown = True
                hand.mouseStartPos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                hand.isDown = False
                hand.mouseStartPos = None
                hand.points = []

    for circle in circles:
        circle.draw()

    if hand.isDown:
        hand.recalculatePoints(circles)

    hand.draw()

    # Update the display (buffer flip)
    displayFPS(screen, 25)
    pygame.display.flip()
    clock.tick(60)

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
