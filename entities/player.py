
import pygame
from core.collision import gerer_collisions, limiter_ecran
from core.types import LARGEUR_ECRAN, HAUTEUR_ECRAN # Ces deux là sont utiles pour limiter_ecran
from entities.base import Entity


class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.Surface((20, 20))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=position)

        self.position = pygame.Vector2(position)
        self.vitesse = pygame.Vector2(0, 0)
        self.vitesse_marche = 5
        self.gravite = 0.8
        self.force_saut = -15

        self.au_sol = False
        self.descend = False

        # --- Variables pour le DOUBLE SAUT ---
        self.sauts_max = 2
        self.sauts_disponibles = self.sauts_max
        self.touche_saut_pressee = False  # Pour éviter de vider les sauts en un clic

    def run(self, plateformes):
        touches = pygame.key.get_pressed()

        # Réinitialise les sauts quand on est au sol
        if self.au_sol:
            self.sauts_disponibles = self.sauts_max

        # Mouvement horizontal
        self.vitesse.x = 0
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.vitesse.x = self.vitesse_marche
        elif touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.vitesse.x = -self.vitesse_marche

        # --- Logique du Saut et Double Saut ---
        # On vérifie si la touche 0 est enfoncée ET si elle ne l'était pas au tour d'avant
        if (touches[pygame.K_KP0] or touches[pygame.K_INSERT]):
            if not self.touche_saut_pressee:
                if self.sauts_disponibles > 0:
                    self.vitesse.y = self.force_saut
                    self.sauts_disponibles -= 1
                    self.au_sol = False
                self.touche_saut_pressee = True
        else:
            self.touche_saut_pressee = False

        # Physique
        self.vitesse.y += self.gravite
        self.descend = touches[pygame.K_s]

        # Appel des fonctions de collision
        gerer_collisions(self, plateformes)
        limiter_ecran(self, LARGEUR_ECRAN, HAUTEUR_ECRAN)

    def draw(self, screen):
        screen.blit(self.image, self.rect)