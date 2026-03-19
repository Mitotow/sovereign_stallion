import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet
import core.constants as constants


def load_player_animations():
    return {
        constants.IDLE: Spritesheet("assets/player/IDLE.png", 96, 96, 0.15),
        constants.RUN: Spritesheet("assets/player/RUN.png", 96, 96, 0.35),
        constants.JUMP: Spritesheet("assets/player/JUMP.png", 96, 96, 0.2, False),
        constants.ATTACK: Spritesheet("assets/player/ATTACK_1.png", 96, 96, 0.3, False),
        constants.HURT: Spritesheet("assets/player/HURT.png", 96, 96, 0.5, False)
    }


class Player(AnimableEntity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        self.animations = load_player_animations()
        super().__init__(screen, position, (256, 256), "IDLE",
                         self.animations, hitbox_size=(75, 100))

        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 300
        self.gravity = 2000
        self.f_jump = -800
        self.is_freeze = False

    def jump(self):
        if self.is_grounded:
            self.velocity.y = self.f_jump
            self.is_grounded = False
            self.set_state(constants.JUMP)

    def attack(self):
        if self.current_state != constants.ATTACK:
            self.is_freeze = True
            self.set_state(constants.ATTACK)

    def take_damage(self, damage: int):
        if self.current_state != constants.HURT:
            self.set_state(constants.HURT)

    def handle_input(self, keys) -> int:
        h_acceleration = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            h_acceleration += self.acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            h_acceleration -= self.acceleration
        if keys[pygame.K_SPACE]:
            self.attack()
        if keys[pygame.K_s]:
            self.take_damage(100)
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

        return h_acceleration

    def move(self, h_acceleration, dt):
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction)
            if abs(self.velocity.x) < 0.5:
                self.velocity.x = 0

    def update_animation(self):
        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)

        if self.velocity.x != 0:
            self.facing_right = is_backward

        speed_ratio = 1
        if (self.current_state == constants.JUMP and self.is_grounded) or \
           (self.is_grounded and self.current_state != constants.ATTACK):
            if abs_velocity_x > 0:
                speed_ratio = (abs_velocity_x / self.max_speed) ** 0.15
                self.set_state(constants.RUN)
            else:
                self.set_state(constants.IDLE)

        self.animate(speed_ratio)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        h_acceleration = self.handle_input(keys)

        # Gestion états bloquants
        if self.current_state in (constants.ATTACK, constants.HURT):
            if self.is_animation_ended():
                self.is_freeze = False
                self.set_state(constants.IDLE)
        else:
            self.move(h_acceleration, dt)

        # Limite vitesse
        if abs(self.velocity.x) > self.max_speed:
            mult = -1 if self.velocity.x < 0 else 1
            self.velocity.x = self.max_speed * mult

        # Si freeze, pas de déplacement
        if self.is_freeze:
            self.velocity.x = 0

        self.update_animation()

    def draw(self):
        self.screen.blit(self.image, self.rect)
