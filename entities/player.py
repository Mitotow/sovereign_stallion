from entities.base import Entity
from core.types import Position
import pygame

# TODO: class Player(Entity)


class Player(Entity):
    def __init__(self, position: Position):
        super().__init__(position)
        self.image: pygame.Surface = pygame.Surface((20, 20))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 5

    def run(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
