import pygame
import math
import core.constants as constants
from core.camera import Camera


class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__()
        self.screen = screen

        # --- PLACEHOLDERS VISUELS ---
        self.image = pygame.Surface((16, 8), pygame.SRCALPHA)  # SRCALPHA pour la transparence si besoin
        self.image.fill((255, 255, 0))  # Jaune (Flèche)

        # On oriente la flèche selon sa direction de mouvement
        angle = math.degrees(math.atan2(velocity.y, velocity.x))
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=position)

        # --- PHYSIQUE & MOUVEMENT ---
        self.position = pygame.Vector2(position)  # On s'assure que c'est une copie
        self.velocity = velocity

        # Hitbox pour le système de collision
        self.hb = self.rect.copy()

        # Variables requises par ton CollisionSystem
        self.is_static = False
        self.gravity = 0
        self.is_grounded = False
        self.hb_x_offset = 0
        self.hb_y_offset = self.rect.height

    def apply_position(self):
        """Méthode appelée par le CollisionSystem pour mettre à jour le rect"""
        self.rect.topleft = self.position
        # On synchronise la hitbox sur la nouvelle position du rect
        self.hb.topleft = self.rect.topleft

    def update(self, dt):
        """
        Le mouvement est géré par CollisionSystem.update().
        Cette méthode sert à nettoyer les projectiles hors écran.
        """
        # Vérification des limites de l'écran
        width = self.screen.get_width()
        height = self.screen.get_height()

        if (self.rect.right < 0 or
                self.rect.left > width or
                self.rect.bottom < 0 or
                self.rect.top > height):
            self.kill()  # Supprime des groupes de sprites

    def draw(self, camera: Camera):
        self.screen.blit(self.image, camera.apply(self.rect))
