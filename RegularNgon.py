import pygame
import math

def get_ngon_points(center, radius, n):
    output = []
    for i in range(n):
        d = (math.cos((i/n)*2*math.pi),math.sin((i/n)*2*math.pi))
        pos = (center[0] + d[0]*radius, center[1] + d[1]*radius)
        output.append(pos)
    return output

def draw_ngon(screen, color, center, radius, n):
    pygame.draw.polygon(
        screen,
        color,
        get_ngon_points(center, radius, n)
    )