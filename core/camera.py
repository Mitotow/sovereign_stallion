import pygame

class Camera:
    def __init__(self, screen: pygame.Surface, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.screen = screen
        self.screen_rect = screen.get_rect()

    def apply(self, entity_rect):
        """Applique le décalage de la caméra à un rectangle"""
        return entity_rect.move(self.camera.topleft)

    def update(self, target):
        """Calcule le décalage pour centrer la caméra sur la cible"""
        # Joueur au milieu de l'écran
        x = -target.rect.centerx + self.screen_rect.centerx
        y = -target.rect.centery + self.screen_rect.centery

        # Empêche la caméra de sortir des limites de la map
        x = min(0, x)
        x = max(-(self.width - self.screen_rect.width), x)
        y = min(0, y)
        y = max(-(self.height - self.screen_rect.height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)