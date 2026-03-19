import pygame
from entities.base import Entity


class Platform(Entity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2,
                 size: tuple, platform_type="solide"):
        super().__init__(screen, position, size)
        self.type = platform_type
        self.is_static = True      # Ne bouge pas
        self.is_solid = True
        self.gravity = 0

    def draw(self):
        color = "red" if self.type == "solide" else "blue"
        pygame.draw.rect(self.screen, color, self.rect)
