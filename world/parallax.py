import pygame
import os


class ParallaxSky:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.base_path = "assets/world/sky"
        self.speeds = [0.05, 0.1, 0.2, 0.4, 0.6]

        # Chargement de tous les layers du ciel
        self.layers = []
        for i in range(5):
            path = os.path.join(self.base_path, f"{i+1}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
            self.layers.append(img)

    def draw(self, camera_x):
        for i, layer in enumerate(self.layers):
            speed = self.speeds[i]
            offset = (camera_x * speed) % self.screen.get_width()
            self.screen.blit(layer, (-offset, 0))
            self.screen.blit(layer, (self.screen.get_width() - offset, 0))