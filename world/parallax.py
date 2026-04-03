import pygame
import os


class ParallaxSky:
    def __init__(self, screen: pygame.Surface):
        self.screen_width = screen.get_width()
        self.base_path = "assets/world/sky"
        self.speeds = [0.005, 0.01, 0.02, 0.04, 0.06]

        # Chargement de tous les layers du ciel
        self.layers = []
        for i in range(5):
            path = os.path.join(self.base_path, f"{i+1}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.screen_width, screen.get_height()))
            self.layers.append(img)

        self.screen_width

    def draw(self, screen, camera_x):
        for i, layer in enumerate(self.layers):
            speed = self.speeds[i]
            offset = (camera_x * speed) % self.screen_width
            screen.blit(layer, (-offset, 0))
            screen.blit(layer, (self.screen_width - offset, 0))