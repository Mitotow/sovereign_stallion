import pygame
from core.constants import SOLID

class Platform:
    def __init__(self, x, y, w, h, platform_type=SOLID, damage=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.hb = self.rect
        self.type = platform_type
        self.is_static = True
        self.is_solid = True
        self.damage = damage
