# menu/main_menu.py
import pygame
from core.image.image_utils import get_image_chunks
import core.constants as constants
from ui.components.button import SelectButton, SelectButtonGroup, ImageButton

BG_IMG_PATH = "assets/ui/main_menu/bg_menu.png"
BUTTONS_IMG_PATH = "assets/ui/main_menu/play_quit_buttons.png"


class MainMenu:
    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen = screen
        self.police = pygame.font.SysFont("Arial", 40)
        self.police_select = pygame.font.SysFont("Arial", 25)
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()
        width_div = self.screen_width // 2
        self.selected_difficulty = constants.DEFAULT_DIFFICULTY

        self.bg_img = pygame.image.load(BG_IMG_PATH)
        self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_width, self.screen_height))

        # Création des boutons
        chunks = get_image_chunks(BUTTONS_IMG_PATH, lig = 2, col = 2, alpha = True)
        self.play_button = ImageButton((width_div - 125, 180), (250, 100), chunks[0], hover_img=chunks[1])
        self.quit_button = ImageButton((width_div - 100, 450), (200, 100), chunks[2], hover_img=chunks[3])

        # Création des boutons de la sélection de difficulté
        select_button_easy = SelectButton("Facile", (width_div - 160, 360), (100, 40), constants.DIFFICULTY_EASY, self.police_select)
        # le bouton normal est sélectionné par défaut : selected = True
        select_button_normal = SelectButton("Normal", (width_div - 50, 360), (100, 40), constants.DIFFICULTY_NORMAL, self.police_select)
        select_button_hard = SelectButton("Difficile", (width_div + 60, 360), (100, 40), constants.DIFFICULTY_HARD, self.police_select)
        self.select_group = SelectButtonGroup([select_button_easy, select_button_normal, select_button_hard], title="Difficulté",
                                                  title_rect=pygame.Rect(
                                                      width_div - 100, 320, 200, 30),
                                                  title_police=self.police_select)
        self.selected_difficulty = self.select_group.get_selected_value()

    def draw(self, surface):
        surface.blit(self.bg_img, (0, 0))

        self.play_button.draw(surface)
        self.select_group.draw(surface)
        self.quit_button.draw(surface)

    def check_click(self):
        if self.play_button.is_clicked():
            return constants.PLAYING
        if self.quit_button.is_clicked():
            return constants.QUIT

        # Mise à jour du groupe de boutons
        if self.select_group.check_click():
            self.selected_difficulty = self.select_group.get_selected_value()

        return constants.MAIN_MENU
