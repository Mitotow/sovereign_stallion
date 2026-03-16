# core/game.py
import pygame
from entities.player import Player
from menu.main_menu import MenuPrincipal
from core.types import LARGEUR_ECRAN, HAUTEUR_ECRAN


class Game():
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.etat = "MENU"
        self.menu = MenuPrincipal()
        self.player = None
        self.plateformes = []

        # --- NOUVEAU PARAMÈTRE ---
        self.difficulte_jeu = None  # Sera réglée au moment de lancer le jeu

    def setup(self, difficulte_choisie):
        # On stocke la difficulté pour savoir comment configurer le niveau
        self.difficulte_jeu = difficulte_choisie

        # Tu peux utiliser la difficulté ici !
        # Par exemple :
        # if self.difficulte_jeu == DIFFICULTE_DIFFICILE:
        #     self.player = Player((100, 100), vitesse_rapide=True)
        # else:

        # Pour l'instant on garde ton setup de base
        self.player = Player(pygame.Vector2(100, 100))

    def run(self):
        while self.isRunning:
            evenements = pygame.event.get()
            for event in evenements:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.etat == "MENU":
                self.menu.dessiner(self.screen)
                choix = self.menu.tester_clic()

                if choix == "JEU_SOLO":
                    # --- NOUVEAU : ON RECUPERE LA DIFFICULTÉ ---
                    diff = self.menu.difficulte_actuelle
                    self.setup(diff)  # On passe le niveau choisi au setup
                    self.etat = "JEU"
                elif choix == "QUITTER":
                    self.isRunning = False

            elif self.etat == "JEU":
                self.screen.fill("black")
                if self.player:
                    self.player.run(self.plateformes)
                    self.player.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()