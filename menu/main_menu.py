# menu/main_menu.py
import pygame
import core.constants as constants
from menu.menu_button import MenuButton, MenuSelectButton, MenuSelectButtonGroup

BD_IMG_PATH = "assets/menu/fond_menu.png"


class MainMenu:
    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen = screen
        self.police = pygame.font.SysFont("Arial", 40)
        self.police_select = pygame.font.SysFont("Arial", 25)
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()
        self.selected_difficulty = constants.DIFFICULTY_NORMAL

        try:
            self.bg_img = pygame.image.load(BD_IMG_PATH)
            self.bg_img = pygame.transform.scale(
                self.bg_img, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            self.bg_img = pygame.Surface(
                (self.screen_width, self.screen_height))
            self.bg_img.fill((30, 30, 30))

        # Création des boutons
        play_button_rect = pygame.Rect(
            self.screen_width // 2 - 125, 180, 250, 60)
        self.play_button = MenuButton("Jouer", play_button_rect, self.police)

        quit_button_rect = pygame.Rect(
            self.screen_width // 2 - 100, 450, 200, 60)
        self.quit_button = MenuButton("Quitter", quit_button_rect, self.police)

        # Création des boutons de la sélection de difficulté
        select_button_easy = MenuSelectButton("Facile", pygame.Rect(
            self.screen_width // 2 - 150, 360, 100, 40), constants.DIFFICULTY_EASY, self.police_select)
        # le bouton normal est sélectionné par défaut : selected = True
        select_button_normal = MenuSelectButton("Normal", pygame.Rect(
            self.screen_width // 2 - 50, 360, 100, 40), constants.DIFFICULTY_NORMAL, self.police_select)
        select_button_hard = MenuSelectButton("Difficile", pygame.Rect(
            self.screen_width // 2 + 50, 360, 100, 40), constants.DIFFICULTY_HARD, self.police_select)
        self.select_group = MenuSelectButtonGroup([select_button_easy, select_button_normal, select_button_hard], title="Difficulté",
                                                  title_rect=pygame.Rect(
                                                      self.screen_width // 2 - 100, 320, 200, 30),
                                                  title_police=self.police_select)
        self.selected_difficulty = self.select_group.get_selected_value()

    def draw(self, surface):
        surface.blit(self.bg_img, (0, 0))

        self.play_button.draw(surface)
        self.select_group.draw(surface)
        self.quit_button.draw(surface)

    def check_click(self):
        click = pygame.mouse.get_pressed()
        if click[0]:  # Clic gauche
            if self.play_button.is_clicked():
                return constants.PLAYING
            if self.quit_button.is_clicked():
                return constants.QUIT

            # Mise à jour du groupe de boutons
            if self.select_group.check_click():
                self.selected_difficulty = self.select_group.get_selected_value()

        return constants.MAIN_MENU
