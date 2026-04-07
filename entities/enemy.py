import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet
import core.constants as constants
from core.camera import Camera

def load_knight_animations():
    return {
        constants.IDLE: Spritesheet("assets/entities/ennemies/test_knight/IDLE.png", 32, 32, 0.15),
    }

class Enemy(AnimableEntity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        super().__init__(screen, position, constants.PLAYER_SIZE, constants.IDLE,
                         load_knight_animations(), hitbox_size=constants.PLAYER_HB_SIZE)
        
        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 150
        self.gravity = 2000
        self.is_freeze = False
        self.is_running = False
        