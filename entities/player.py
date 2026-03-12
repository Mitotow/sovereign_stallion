from entities.base import Entity
from core.types import Position
import pygame

# TODO: class Player(Entity)


class Player(Entity):
    def __init__(self, position: Position):
        super().__init__(position)
        self.image: pygame.Surface = pygame.Surface((100, 100))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=position)

        # deplacements
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 2000
        self.friction = 0.25
        self.max_speed = 300
        self.gravity = 2000  # Force d'attraction
        self.f_jump = -450  # Impulsion
        self.is_grounded = False

    def jump(self):
        if self.is_grounded:
            self.velocity.y = self.f_jump
            self.is_grounded = False

    def update_grounded(self, screen: pygame.Surface):
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.velocity.y = 0
            self.is_grounded = True

    def run(self, dt, screen):
        keys = pygame.key.get_pressed()
        h_acceleration = 0  # init acceleration à 0

        # Prise en compte de la gravité
        self.velocity.y += self.gravity * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            h_acceleration += self.acceleration

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            h_acceleration -= self.acceleration

        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

        self.velocity.x += h_acceleration * dt
        self.velocity.x *= (1 - self.friction)

        if abs(self.velocity.x) > self.max_speed:
            mult = -1 if self.velocity.x < 0 else 1
            self.velocity.x = self.max_speed * mult

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        self.update_grounded(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
