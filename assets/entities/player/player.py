import pygame
from entities.base import Entity
from core.types import Position


class Player(Entity):
    def __init__(self, position: Position):
        super().__init__(position)

        # 1. On charge la grande planche (le "film" de l'animation)
        self.sprite_sheet = pygame.image.load("assets/run.png").convert_alpha()

        # 2. On définit la taille d'une seule image (ex: 64x64 pixels)
        self.frame_width = 64
        self.frame_height = 64

        # 3. On crée une liste pour stocker nos "découpes"
        self.images_run = []
        for i in range(4):  # Si tu as 4 images dans ton animation de course
            # On découpe un carré de 64x64 en décalant X à chaque fois (0, 64, 128, 192)
            surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            surface.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.images_run.append(surface)

        # 4. Variables pour gérer le défilement
        self.index = 0
        self.image = self.images_run[self.index]
        self.rect = self.image.get_rect(topleft=position)

    def animate(self):
        # On augmente l'index un tout petit peu à chaque image (ex: 0.1)
        # Si on l'augmentait de 1, l'animation irait beaucoup trop vite !
        self.index += 0.1

        # Si l'index arrive à la fin de la liste (4), on revient à 0
        if self.index >= len(self.images_run):
            self.index = 0

        # On met à jour l'image affichée (on transforme 1.2 en 1 pour la liste)
        self.image = self.images_run[int(self.index)]

    def run(self):
        # Quand le joueur bouge, on appelle l'animation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # Droite
            self.rect.x += 5
            self.animate()