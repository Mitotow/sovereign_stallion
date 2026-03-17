from pygame import Surface, Rect
from pygame.font import Font

def blit_text_center(surface: Surface, text: str, rect: Rect, police: Font, color=(255, 255, 255)):
        """ Centrer le texte dans un rectangle. """
        txt_surface = police.render(text, True, color)
        txt_rect = txt_surface.get_rect()
        txt_rect.center = rect.center
        surface.blit(txt_surface, txt_rect)
        
def blit_text(surface: Surface, text: str, position: tuple[int, int], police: Font, color=(255, 255, 255)):
        txt_surface: Surface = police.render(text, True, color)
        txt_rect = txt_surface.get_rect()
        txt_rect.topleft = position
        surface.blit(txt_surface, txt_rect)