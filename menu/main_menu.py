# menu/main_menu.py
import pygame
from core.types import LARGEUR_ECRAN, HAUTEUR_ECRAN, DIFFICULTE_FACILE, DIFFICULTE_NORMALE, DIFFICULTE_DIFFICILE


class MenuPrincipal:
    def __init__(self):
        pygame.font.init()
        self.police = pygame.font.SysFont("Arial", 40)
        self.police_difficulte = pygame.font.SysFont("Arial", 25)

        # --- NOUVEAU : CHARGEMENT DU FOND ---
        # Assure-toi d'avoir une image "fond_menu.png" dans le dossier de ton projet !
        try:
            self.image_fond = pygame.image.load("fond_menu.png")
            # On redimensionne l'image pour qu'elle corresponde à l'écran
            self.image_fond = pygame.transform.scale(self.image_fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        except FileNotFoundError:
            print("Image 'fond_menu.png' non trouvée. Utilisation d'un fond de secours.")
            self.image_fond = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN))
            self.image_fond.fill((30, 30, 30))

        # --- NOUVEAUX BOUTONS ---
        # Centrés
        self.bouton_jouer = pygame.Rect(LARGEUR_ECRAN // 2 - 125, 180, 250, 60)
        self.bouton_multijoueur = pygame.Rect(LARGEUR_ECRAN // 2 - 125, 260, 250, 60)

        # Difficultés (Alignées horizontalement)
        self.rects_difficulte = {
            DIFFICULTE_FACILE: pygame.Rect(LARGEUR_ECRAN // 2 - 150, 360, 100, 40),
            DIFFICULTE_NORMALE: pygame.Rect(LARGEUR_ECRAN // 2 - 50, 360, 100, 40),
            DIFFICULTE_DIFFICILE: pygame.Rect(LARGEUR_ECRAN // 2 + 50, 360, 100, 40),
        }

        self.bouton_quitter = pygame.Rect(LARGEUR_ECRAN // 2 - 100, 450, 200, 60)

        self.couleur_bouton = (50, 50, 50)
        self.couleur_survol = (100, 100, 100)
        self.couleur_selection = (50, 200, 50)  # Vert pour la difficulté sélectionnée
        self.couleur_texte = (255, 255, 255)

        self.difficulte_actuelle = DIFFICULTE_NORMALE  # Sélection par défaut

    def dessiner(self, surface):
        surface.blit(self.image_fond, (0, 0))  # Fond en premier

        souris_pos = pygame.mouse.get_pos()

        # --- Dessin BOUTON JOUER ---
        couleur = self.couleur_survol if self.bouton_jouer.collidepoint(souris_pos) else self.couleur_bouton
        pygame.draw.rect(surface, couleur, self.bouton_jouer, border_radius=10)
        self.blit_texte_centre(surface, "SOLO", self.bouton_jouer, self.police)

        # --- Dessin BOUTON MULTIJOUEUR ---
        couleur = self.couleur_survol if self.bouton_multijoueur.collidepoint(souris_pos) else self.couleur_bouton
        pygame.draw.rect(surface, couleur, self.bouton_multijoueur, border_radius=10)
        self.blit_texte_centre(surface, "MULTIJOUEUR", self.bouton_multijoueur, self.police)

        # --- Dessin SELECTEUR DE DIFFICULTÉ ---
        self.blit_texte_centre(surface, "DIFFICULTÉ :", pygame.Rect(LARGEUR_ECRAN // 2 - 100, 320, 200, 30),
                               self.police_difficulte)

        noms_diff = {DIFFICULTE_FACILE: "FACILE", DIFFICULTE_NORMALE: "NORMAL", DIFFICULTE_DIFFICILE: "DIFFICILE"}

        for niv, rect in self.rects_difficulte.items():
            # Couleur change si sélectionné ou survolé
            if niv == self.difficulte_actuelle:
                couleur = self.couleur_selection
            elif rect.collidepoint(souris_pos):
                couleur = self.couleur_survol
            else:
                couleur = self.couleur_bouton

            pygame.draw.rect(surface, couleur, rect, border_radius=8)
            self.blit_texte_centre(surface, noms_diff[niv], rect, self.police_difficulte)

        # --- Dessin BOUTON QUITTER ---
        couleur = self.couleur_survol if self.bouton_quitter.collidepoint(souris_pos) else self.couleur_bouton
        pygame.draw.rect(surface, couleur, self.bouton_quitter, border_radius=10)
        self.blit_texte_centre(surface, "QUITTER", self.bouton_quitter, self.police)

    def tester_clic(self):
        souris_pos = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()

        if clic[0]:  # Clic gauche
            if self.bouton_jouer.collidepoint(souris_pos):
                return "JEU_SOLO"
            if self.bouton_multijoueur.collidepoint(souris_pos):
                return "JEU_MULTI"  # (Pas encore implémenté)
            if self.bouton_quitter.collidepoint(souris_pos):
                return "QUITTER"

            # Gestion des clics de difficulté
            for niv, rect in self.rects_difficulte.items():
                if rect.collidepoint(souris_pos):
                    self.difficulte_actuelle = niv
                    return "MENU"  # Reste sur le menu

        return "MENU"

    def blit_texte_centre(self, surface, texte, rect, police):
        """Petite fonction pour centrer le texte dans un rectangle."""
        txt_surface = police.render(texte, True, self.couleur_texte)
        txt_rect = txt_surface.get_rect()
        txt_rect.center = rect.center
        surface.blit(txt_surface, txt_rect)