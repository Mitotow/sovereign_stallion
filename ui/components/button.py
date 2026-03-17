import pygame
from ui.ui_utils import blit_text_center

class BaseButton:
    """Classe de base pour tous les boutons du jeu."""

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        """
        Initialise un bouton de base.

        Args:
            position (tuple[int, int]): Position (x, y) du coin supérieur gauche du bouton
            size (tuple[int, int]): Taille (largeur, hauteur) du bouton
        """
        self.rect = pygame.Rect(*position, *size)

    def draw(self, _: pygame.Surface):
        """
        Dessine le bouton sur la surface donnée.
        À surcharger dans les classes dérivées.

        Args:
            _ (pygame.Surface): Surface sur laquelle dessiner le bouton
        """
        pass

    def is_hover(self) -> bool:
        """
        Vérifie si le curseur de la souris est au-dessus du bouton.

        Returns:
            bool: True si la souris est au-dessus du bouton, False sinon
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self) -> bool:
        """
        Vérifie si le bouton est cliqué (bouton gauche de la souris enfoncé).

        Returns:
            bool: True si le bouton est cliqué, False sinon
        """
        return pygame.mouse.get_pressed()[0] and self.is_hover()

class Button(BaseButton):
    """Bouton standard avec texte."""

    def __init__(self, title: str, position: tuple[int, int], size: tuple[int, int], police: pygame.font.Font,
                 color=(50, 50, 50), color_hover=(100, 100, 100),
                 border_radius=10):
        """
        Initialise un bouton avec texte.

        Args:
            title (str): Texte à afficher sur le bouton
            position (tuple[int, int]): Position du bouton
            size (tuple[int, int]): Taille du bouton
            police (pygame.font.Font): Police de caractères pour le texte
            color (tuple[int, int, int]): Couleur de base du bouton (RGB)
            color_hover (tuple[int, int, int]): Couleur quand la souris est au-dessus (RGB)
            border_radius (int): Rayon des coins arrondis
        """
        super().__init__(position, size)
        self.title = title
        self.color = color
        self.color_hover = color_hover
        self.border_radius = border_radius
        self.police = police

    def draw(self, surface: pygame.Surface):
        """
        Dessine le bouton sur la surface donnée.

        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner le bouton
        """
        mouse_pos = pygame.mouse.get_pos()
        couleur = self.color_hover if self.rect.collidepoint(
            mouse_pos) else self.color
        pygame.draw.rect(surface, couleur, self.rect,
                         border_radius=self.border_radius)
        blit_text_center(surface, self.title, self.rect, self.police)

class SelectButton(Button):
    """Bouton de sélection qui peut être sélectionné parmi un groupe."""

    def __init__(self, title, position: tuple[int, int], size: tuple[int, int], value,
                 police: pygame.font.Font, color_hover=(0, 0, 0), color_selected=(0, 0, 0)):
        """
        Initialise un bouton de sélection.

        Args:
            title (str): Texte à afficher sur le bouton
            position (tuple[int, int]): Position du bouton
            size (tuple[int, int]): Taille du bouton
            value: Valeur associée au bouton
            police (pygame.font.Font): Police de caractères
            color_hover (tuple[int, int, int]): Couleur au survol
            color_selected (tuple[int, int, int]): Couleur quand sélectionné
        """
        super().__init__(title, position, size, police, color_hover)
        self.value = value
        self.selected = False
        self.color_selected = color_selected

    def draw(self, surface):
        """
        Dessine le bouton de sélection avec la couleur appropriée.

        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        color = self.color
        if self.selected:
            color = self.color_selected
        elif self.color_hover and self.is_hover():
            color = self.color_hover

        pygame.draw.rect(surface, color, self.rect,
                         border_radius=self.border_radius)

        blit_text_center(surface, self.title, self.rect, self.police)

class SelectButtonGroup:
    """Groupe de boutons de sélection où un seul peut être sélectionné à la fois."""

    def __init__(self, buttons: list[SelectButton], title: str | None = None,
                 title_rect: pygame.Rect | None = None,
                 title_police: pygame.font.Font | None = None):
        """
        Initialise un groupe de boutons de sélection.

        Args:
            buttons (list[SelectButton]): Liste des boutons du groupe
            title (str | None): Titre optionnel du groupe
            title_rect (pygame.Rect | None): Rectangle pour le titre
            title_police (pygame.font.Font | None): Police pour le titre
        """
        self.buttons = buttons
        self.title = title
        self.title_rect = title_rect
        self.title_police = title_police

    def draw(self, surface: pygame.Surface):
        """
        Dessine le groupe de boutons et son titre.

        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        if self.title and self.title_rect:
            blit_text_center(surface, self.title,
                              self.title_rect, self.title_police)

        for button in self.buttons:
            button.draw(surface)

    def get_selected_value(self) -> str | None:
        """
        Récupère la valeur du bouton sélectionné.

        Returns:
            str | None: Valeur du bouton sélectionné ou None si aucun n'est sélectionné
        """
        for button in self.buttons:
            if button.selected:
                return button.value

        return None

    def set_selected(self, value):
        """
        Sélectionne le bouton avec la valeur spécifiée.

        Args:
            value: Valeur du bouton à sélectionner
        """
        for button in self.buttons:
            if button.value == value:
                button.selected = True
            if button.selected and button.value != value:
                button.selected = False

    def check_click(self):
        """
        Vérifie si un bouton du groupe a été cliqué et met à jour la sélection.

        Returns:
            bool: True si un bouton a été cliqué, False sinon
        """
        for button in self.buttons:
            if button.is_clicked():
                self.set_selected(button.value)
                return True

        return False

class ImageButton(BaseButton):
    """Bouton utilisant une image comme fond."""

    def __init__(self, position: tuple[int, int], size: tuple[int, int],
                 img: pygame.Surface, active_img: pygame.Surface | None = None,
                 hover_img: pygame.Surface | None = None):
        """
        Initialise un bouton avec image.

        Args:
            position (tuple[int, int]): Position du bouton
            size (tuple[int, int]): Taille du bouton
            img (pygame.Surface): Image de base du bouton
            active_img (pygame.Surface | None): Image quand le bouton est actif
            hover_img (pygame.Surface | None): Image quand la souris est au-dessus
        """
        super().__init__(position, size)
        self.image = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        self.active_img = hover_img
        self.hover_img = pygame.transform.scale(hover_img, (self.rect.width, self.rect.height))
        self.is_active = False

    def draw(self, surface: pygame.Surface):
        """
        Dessine le bouton image sur la surface.

        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        curr_img = self.image
        if self.is_hover():
            curr_img = self.hover_img
        surface.blit(curr_img, self.rect)

class SelectImageButton(SelectButton):
    """Bouton de sélection utilisant une image comme fond."""

    def __init__(self, title, position: tuple[int, int], size: tuple[int, int], value,
                 police: pygame.font.Font, color_hover=(0, 0, 0), color_selected=(0, 0, 0)):
        """
        Initialise un bouton de sélection avec image.

        Args:
            title (str): Texte à afficher
            position (tuple[int, int]): Position du bouton
            size (tuple[int, int]): Taille du bouton
            value: Valeur associée au bouton
            police (pygame.font.Font): Police de caractères
            color_hover (tuple[int, int, int]): Couleur au survol
            color_selected (tuple[int, int, int]): Couleur quand sélectionné
        """
        super().__init__(title, position, size, value, police, color_hover)
        self.value = value
        self.selected = False
        self.color_selected = color_selected

    def draw(self, surface):
        """
        Dessine le bouton de sélection image.

        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
        """
        curr_img = self.image
        if self.is_hover():
            curr_img = self.hover_img
        surface.blit(curr_img, self.rect)
