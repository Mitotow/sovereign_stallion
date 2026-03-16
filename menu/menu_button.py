import pygame
from menu.menu_utils import blit_texte_centre


class MenuButton:
    def __init__(self, title: str, rect: pygame.Rect, police: pygame.font.Font,
                 color=(50, 50, 50), color_hover=(100, 100, 100),
                 border_radius=10):
        self.title = title
        self.rect = rect
        self.color = color
        self.color_hover = color_hover
        self.border_radius = border_radius
        self.police = police

    def draw(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        couleur = self.color_hover if self.rect.collidepoint(
            mouse_pos) else self.color
        pygame.draw.rect(surface, couleur, self.rect,
                         border_radius=self.border_radius)
        blit_texte_centre(surface, self.title, self.rect, self.police)

    def is_clicked(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class MenuSelectButton(MenuButton):
    def __init__(self, title, rect, value, police: pygame.font.Font,
                 color_selected=(0, 0, 0)):
        super().__init__(title, rect, police)
        self.value = value
        self.selected = False
        self.color_selected = color_selected

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_selected if self.selected
                         else self.color, self.rect,
                         border_radius=self.border_radius)
        blit_texte_centre(surface, self.title, self.rect, self.police)


class MenuSelectButtonGroup:
    def __init__(self, buttons: list[MenuSelectButton], title: str | None = None,
                 title_rect: pygame.Rect | None = None,
                 title_police: pygame.font.Font | None = None):
        self.buttons = buttons
        self.title = title
        self.title_rect = title_rect
        self.title_police = title_police

    def draw(self, surface: pygame.Surface):
        if self.title and self.title_rect:
            blit_texte_centre(surface, self.title,
                              self.title_rect, self.title_police)

        for button in self.buttons:
            button.draw(surface)

    def get_selected_value(self) -> str | None:
        for button in self.buttons:
            if button.selected:
                return button.value

        return None

    def set_selected(self, value):
        for button in self.buttons:
            if button.value == value:
                button.selected = True
            if button.selected and button.value != value:
                button.selected = False

    def check_click(self):
        for button in self.buttons:
            if button.is_clicked():
                self.set_selected(button.value)
                return True

        return False

