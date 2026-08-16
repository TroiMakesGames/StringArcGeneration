import math

def circularArc(p1, p2, focusLength, t, flip=False):

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