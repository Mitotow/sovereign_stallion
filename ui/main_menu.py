# menu/main_menu.py
import pygame
from core.image.image_utils import get_image_chunks
import core.constants as constants
from ui.components.button import SelectButton, SelectButtonGroup, ImageButton
from ui.menu import Menu

BG_IMG_PATH = "assets/ui/main_menu/bg_menu.png"
BUTTONS_IMG_PATH = "assets/ui/main_menu/play_quit_buttons.png"


class MainMenu(Menu):
    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen = screen
        self.police = pygame.font.SysFont("Arial", 40)
        self.police_select = pygame.font.SysFont("Arial", 25)
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()
        centerx = self.screen.get_rect().centerx
        self.selected_difficulty = constants.DEFAULT_DIFFICULTY

        self.bg_img = pygame.image.load(BG_IMG_PATH)
        self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_width, self.screen_height))

        # Création des boutons
        chunks = get_image_chunks(BUTTONS_IMG_PATH, lig = 2, col = 2, alpha = True)
        self.play_button = ImageButton((centerx - 125, 180), (250, 100), chunks[0], hover_img=chunks[1])
        self.quit_button = ImageButton((centerx - 100, 450), (200, 100), chunks[2], hover_img=chunks[3])

        # Création des boutons de la sélection de difficulté
        select_button_easy = SelectButton("Facile", (centerx - 160, 360), (100, 40), constants.DIFFICULTY_EASY, self.police_select)
        # le bouton normal est sélectionné par défaut : selected = True
        select_button_normal = SelectButton("Normal", (centerx - 50, 360), (100, 40), constants.DIFFICULTY_NORMAL, self.police_select)
        select_button_hard = SelectButton("Difficile", (centerx + 60, 360), (100, 40), constants.DIFFICULTY_HARD, self.police_select)
        self.select_group = SelectButtonGroup([select_button_easy, select_button_normal, select_button_hard], title="Difficulté",
                                                  title_rect=pygame.Rect(
                                                      centerx - 100, 320, 200, 30),
                                                  title_police=self.police_select)
        self.selected_difficulty = self.select_group.get_selected_value()
        
    def update(self):
        return self.check_click()

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))

        self.play_button.draw(self.screen)
        self.select_group.draw(self.screen)
        self.quit_button.draw(self.screen)

    def check_click(self):
        if self.play_button.is_clicked():
            return constants.PLAYING
        if self.quit_button.is_clicked():
            return constants.QUIT

        # Mise à jour du groupe de boutons
        if self.select_group.check_click():
            self.selected_difficulty = self.select_group.get_selected_value()

        return constants.MAIN_MENU
