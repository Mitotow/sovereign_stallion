import pygame
import math
from entities.projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    """Classe parente qui contient les fonctions communes"""

    def __init__(self, screen, position):
        super().__init__()
        self.screen = screen
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 2000
        self.is_static = False
        self.is_grounded = False
        self.hb_x_offset = 0

    def apply_position(self):
        """Met à jour le rectangle et la hitbox"""
        self.rect.topleft = self.position
        self.hb.topleft = self.rect.topleft

    def draw(self):
        """Affiche l'ennemi à l'écran (C'est cette fonction qui manquait !)"""
        self.screen.blit(self.image, self.rect)


class Archer(Enemy):
    """L'ennemi rouge qui tire"""

    def __init__(self, screen, position):
        super().__init__(screen, position)
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 0, 0))  # ROUGE
        self.rect = self.image.get_rect(topleft=position)
        self.hb = self.rect.copy()
        self.hb_y_offset = self.rect.height
        self.attack_timer = 0

    def update(self, dt, game):
        self.attack_timer += dt
        if not self.is_grounded:
            self.velocity.y += self.gravity * dt

        # Tir toutes les 2 secondes
        if self.attack_timer >= 2.0:
            self.shoot(game)
            self.attack_timer = 0

    def shoot(self, game):
        p_pos = pygame.Vector2(game.player.rect.center)
        e_pos = pygame.Vector2(self.rect.center)
        direction = (p_pos - e_pos)
        if direction.length() > 0:
            direction = direction.normalize()

        # On crée la flèche
        arrow = Projectile(self.screen, e_pos, direction * 400)
        game.projectiles.add(arrow)
        game.collision_system.add_dynamic(arrow)


class Knight(Enemy):
    """L'ennemi noir qui poursuit"""

    def __init__(self, screen, position):
        super().__init__(screen, position)
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 0))  # NOIR
        self.rect = self.image.get_rect(topleft=position)
        self.hb = self.rect.copy()
        self.hb_y_offset = self.rect.height
        self.speed = 120

    def update(self, dt, game):
        if not self.is_grounded:
            self.velocity.y += self.gravity * dt

        # IA de poursuite
        dx = game.player.rect.centerx - self.rect.centerx
        if abs(dx) > 40:
            self.velocity.x = self.speed if dx > 0 else -self.speed
        else:
            self.velocity.x = 0