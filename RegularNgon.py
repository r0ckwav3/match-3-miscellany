import pygame
import math

def get_ngon_points(center, radius, n, rot_offset=0):
    output = []
    for i in range(n):
        d = (math.cos(rot_offset + (i/n)*2*math.pi),math.sin(rot_offset + (i/n)*2*math.pi))
        pos = (center[0] + d[0]*radius, center[1] + d[1]*radius)
        output.append(pos)
    return output

def draw_ngon(screen, color, center, radius, n, rot_offset=0):
    pygame.draw.polygon(
        screen,
        color,
        get_ngon_points(center, radius, n, rot_offset)
    )

def draw_rotated_rect(screen, color, center, width, height, rot):
    wvec = (math.cos(rot)*width/2, math.sin(rot)*width/2)
    hvec = (math.cos(rot+math.pi/2)*height/2, math.sin(rot+math.pi/2)*height/2)
    verts = [
        (wvec[0] + hvec[0], wvec[1] + hvec[1]),
        (wvec[0] - hvec[0], wvec[1] - hvec[1]),
        (-wvec[0] - hvec[0], -wvec[1] - hvec[1]),
        (-wvec[0] + hvec[0], -wvec[1] + hvec[1])
    ]
    pygame.draw.polygon(
        screen,
        color,
        verts
    )
