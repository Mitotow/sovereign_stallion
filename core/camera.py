import pygame

class Camera:
    def __init__(self, width, height, screen_width, screen_height):
        # Le rectangle de la caméra définit la zone de la map
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, entity_rect):
        """Applique le décalage de la caméra à un rectangle (joueur, objet, etc.)"""
        return entity_rect.move(self.camera.topleft)

    def update(self, target):
        """Calcule le décalage pour centrer la caméra sur la cible (le joueur)"""
        # On veut que le joueur soit au milieu de l'écran
        x = -target.rect.centerx + int(self.screen_width / 2)
        y = -target.rect.centery + int(self.screen_height / 2)

        # --- CLAMPING (Butées) ---
        # Empêche la caméra de sortir des limites de la map
        x = min(0, x) # Bord gauche
        x = max(-(self.width - self.screen_width), x) # Bord droit
        y = min(0, y) # Bord haut
        y = max(-(self.height - self.screen_height), y) # Bord bas

        self.camera = pygame.Rect(x, y, self.width, self.height)